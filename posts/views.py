from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post


def inicio(request):
    return render(request, "posts/inicio.html")


def acerca(request):
    return render(request, "posts/acerca.html")


def lista_posts(request):
    posts = Post.objects.filter(estado=Post.PUBLICADO).order_by("-fecha_creacion")
    promedio = posts.aggregate(promedio=Avg("likes"))["promedio"] or 0
    mas_popular = posts.order_by("-likes").first()
    context = {
        "posts": posts,
        "promedio": round(promedio, 1),
        "mas_popular": mas_popular,
    }
    return render(request, "posts/lista_posts.html", context)


def detalle_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "posts/detalle.html", {"post": post})


def nuevo_post(request):
    form = PostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("lista_posts")
    return render(request, "posts/nuevo.html", {"form": form})
