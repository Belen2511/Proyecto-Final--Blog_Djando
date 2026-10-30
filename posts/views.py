from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from guardian.shortcuts import assign_perm, get_objects_for_user, get_users_with_perms, remove_perm

from .forms import BuscarForm, CompartirForm, ContactoForm, PostForm
from .models import Post

User = get_user_model()


# ---------------------------------------------------------------------------
# Autorización
# ---------------------------------------------------------------------------
def puede_modificar(user, post):
    """¿Este usuario puede editar o eliminar este post? Tres caminos:
    1. es el autor,
    2. tiene el permiso GLOBAL posts.change_post (por ejemplo, el grupo Editores),
    3. tiene el permiso sobre ESTE post (se lo compartieron: django-guardian).

    Ojo: un permiso global NO implica el de objeto, y al revés. Por eso se preguntan los dos."""
    return user.is_authenticated and (
        post.autor_id == user.id
        or user.has_perm("posts.change_post")
        or user.has_perm("posts.change_post", post)
    )


def es_editor(user):
    """Regla sobre la PERSONA (no sobre un objeto): pertenece al grupo Editores."""
    return user.groups.filter(name="Editores").exists()


# ---------------------------------------------------------------------------
# Páginas y CRUD con funciones
# ---------------------------------------------------------------------------
def inicio(request):
    return render(request, "posts/inicio.html")


def acerca(request):
    return render(request, "posts/acerca.html")


def lista_posts(request):
    posts = Post.objects.select_related("autor").all()  # select_related => JOIN para optimizar consultas
    form = BuscarForm(request.GET or None)  # GET: unbound si no hay parámetros
    if form.is_valid():
        q = form.cleaned_data["q"]
        autor = form.cleaned_data["autor"]
        if q:
            posts = posts.filter(titulo__icontains=q)
        if autor:
            posts = posts.filter(autor__username__icontains=autor)
    return render(request, "posts/lista_posts.html", {"posts": posts, "form": form})


@login_required
def mis_posts(request):
    propios = Post.objects.filter(autor=request.user)
    # Posts que otra persona me compartió (permiso por objeto). accept_global_perms=False:
    # sin eso, un Editor (permiso global) vería TODOS los posts como "compartidos".
    compartidos = (
        get_objects_for_user(request.user, "posts.change_post", klass=Post, accept_global_perms=False)
        .exclude(autor=request.user)
    )
    return render(request, "posts/mis_posts.html", {"posts": propios, "compartidos": compartidos})


def detalle_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "posts/detalle_post.html", {
        "post": post,
        "puede_modificar": puede_modificar(request.user, post),
        "es_autor": request.user.is_authenticated and post.autor_id == request.user.id,
    })


@login_required
def crear_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            messages.success(request, "Post creado.")
            return redirect("detalle_post", slug=post.slug)
    else:
        form = PostForm(user=request.user)
    return render(request, "posts/post_form.html", {
        "form": form, "titulo_pagina": "Crear post", "texto_boton": "Crear",
    })


@login_required
def editar_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not puede_modificar(request.user, post):
        raise PermissionDenied
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post, user=request.user)  # instance => UPDATE
        if form.is_valid():
            form.save()
            messages.success(request, "Cambios guardados.")
            return redirect("detalle_post", slug=post.slug)
    else:
        form = PostForm(instance=post, user=request.user)
    return render(request, "posts/post_form.html", {
        "form": form, "titulo_pagina": "Editar post", "texto_boton": "Guardar cambios",
    })


@login_required
def eliminar_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not puede_modificar(request.user, post):
        raise PermissionDenied
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post eliminado.")
        return redirect("lista_posts")
    return render(request, "posts/post_confirm_delete.html", {"post": post})


# ---------------------------------------------------------------------------
# Decoradores: permission_required y user_passes_test
# ---------------------------------------------------------------------------
@login_required                                                   # sin sesión -> pantalla de login
@permission_required("posts.change_post", raise_exception=True)   # con sesión y sin permiso -> 403
def borradores(request):
    """Permiso GLOBAL. Con raise_exception=True, quien está logueado sin el permiso recibe 403.
    Pero el anónimo TAMBIÉN recibiría 403; por eso se apila @login_required arriba."""
    posts = Post.objects.filter(estado=Post.BORRADOR).select_related("autor")
    return render(request, "posts/lista_protegida.html", {
        "titulo": "Borradores",
        "mecanismo": "@permission_required('posts.change_post', raise_exception=True)",
        "posts": posts,
    })


@user_passes_test(es_editor)
def panel_editores(request):
    """Condición sobre el usuario: es del grupo Editores. Si no cumple, REDIRIGE al login
    (aunque ya esté logueado). El decorador solo recibe al usuario, nunca al objeto."""
    posts = Post.objects.select_related("autor")
    return render(request, "posts/lista_protegida.html", {
        "titulo": "Panel de editores (todos los posts)",
        "mecanismo": "@user_passes_test(es_editor)",
        "posts": posts,
    })


# ---------------------------------------------------------------------------
# Permisos por objeto (django-guardian): compartir un post
# ---------------------------------------------------------------------------
@login_required
def compartir_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.autor_id != request.user.id:
        raise PermissionDenied  # solo el autor comparte; un colaborador no puede re-compartir
    if request.method == "POST":
        form = CompartirForm(request.POST, post=post)
        if form.is_valid():
            usuario = form.cleaned_data["usuario"]
            assign_perm("change_post", usuario, post)  # permiso solo sobre ESTE post
            messages.success(request, f"Ahora {usuario.username} puede editar este post.")
            return redirect("compartir_post", slug=post.slug)
    else:
        form = CompartirForm(post=post)
    colaboradores = get_users_with_perms(post, only_with_perms_in=["change_post"], with_group_users=False)
    return render(request, "posts/compartir.html", {
        "post": post, "form": form, "colaboradores": colaboradores,
    })


@login_required
@require_POST
def quitar_colaborador(request, slug, username):
    post = get_object_or_404(Post, slug=slug)
    if post.autor_id != request.user.id:
        raise PermissionDenied
    usuario = get_object_or_404(User, username=username)
    remove_perm("change_post", usuario, post)
    messages.success(request, f"{usuario.username} ya no puede editar este post.")
    return redirect("compartir_post", slug=post.slug)


# ---------------------------------------------------------------------------
# El resto
# ---------------------------------------------------------------------------
def estadisticas(request):
    """Equivalente a la opción 5 del menú de consola, pero con el ORM."""
    posts = Post.objects.all()
    contexto = {
        "total": posts.count(),
        "promedio": posts.aggregate(p=Avg("likes"))["p"],
        "mas_popular": posts.order_by("-likes").first(),
    }
    return render(request, "posts/estadisticas.html", contexto)


def contacto(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            return render(request, "posts/contacto_exito.html", {"nombre": nombre})
    else:
        form = ContactoForm()
    return render(request, "posts/contacto.html", {"form": form})
