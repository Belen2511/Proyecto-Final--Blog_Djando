from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BuscarForm, ContactoForm, PostForm
from .models import Post


def inicio(request):
    return render(request, "posts/inicio.html")


def acerca(request):
    return render(request, "posts/acerca.html")


def lista_posts(request):
    posts = Post.objects.all()
    form = BuscarForm(request.GET or None)  # GET: unbound si no hay parámetros
    if form.is_valid():
        q = form.cleaned_data["q"]
        autor = form.cleaned_data["autor"]
        if q:
            posts = posts.filter(titulo__icontains=q)
        if autor:
            posts = posts.filter(autor__iexact=autor)
    return render(request, "posts/lista_posts.html", {"posts": posts, "form": form})


def detalle_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "posts/detalle_post.html", {"post": post})


def crear_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect("detalle_post", slug=post.slug)
    else:
        form = PostForm()
    return render(request, "posts/post_form.html", {
        "form": form, "titulo_pagina": "Crear post", "texto_boton": "Crear",
    })


def editar_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)  # instance => UPDATE, no INSERT
        if form.is_valid():
            form.save()
            return redirect("detalle_post", slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, "posts/post_form.html", {
        "form": form, "titulo_pagina": "Editar post", "texto_boton": "Guardar cambios",
    })


def eliminar_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
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
