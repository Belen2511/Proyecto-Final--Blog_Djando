from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .forms import BuscarForm, ContactoForm, PostForm
from .models import Post


def puede_modificar(user, post):
    """Autorización: ¿este usuario puede editar o eliminar este post?
    - el autor, siempre
    - o quien tenga el permiso 'posts.change_post' (por ejemplo, el grupo Editores)."""
    return user.is_authenticated and (post.autor_id == user.id or user.has_perm("posts.change_post"))

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
    posts = Post.objects.filter(autor=request.user)
    return render(request, "posts/mis_posts.html", {"posts": posts})


def detalle_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "posts/detalle_post.html", {
        "post": post,
        "puede_modificar": puede_modificar(request.user, post),
    })

@login_required
def crear_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  
            post.autor = request.user       
            post.save() 
            return redirect("detalle_post", slug=post.slug)
            
    else:
        form = PostForm()
    return render(request, "posts/post_form.html", {
        "form": form, "titulo_pagina": "Crear post", "texto_boton": "Crear",
    })

@login_required
def editar_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not puede_modificar(request.user, post):
        raise PermissionDenied 
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)  # instance => UPDATE, no INSERT
        if form.is_valid():
            form.save()
            return redirect("detalle_post", slug=post.slug)
    else:
        form = PostForm(instance=post)
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
        return redirect("lista_posts")
    return render(request, "posts/post_confirm_delete.html", {"post": post})


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
