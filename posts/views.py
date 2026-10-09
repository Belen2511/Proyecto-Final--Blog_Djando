from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post

POSTS_POR_PAGINA = 5


def inicio(request):
    return render(request, "posts/inicio.html")


def acerca(request):
    return render(request, "posts/acerca.html")


def lista_posts(request):
    posts = Post.objects.filter(estado=Post.PUBLICADO).order_by("-fecha_creacion")
    promedio = posts.aggregate(promedio=Avg("likes"))["promedio"] or 0
    mas_popular = posts.order_by("-likes").first()
    page_obj = Paginator(posts, POSTS_POR_PAGINA).get_page(request.GET.get("page"))
    context = {
        "posts": page_obj,
        "page_obj": page_obj,
        "promedio": round(promedio, 1),
        "mas_popular": mas_popular,
    }
    return render(request, "posts/lista_posts.html", context)


def detalle_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "posts/detalle.html", {"post": post})


def nuevo_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_posts")
    else:
        form = PostForm()
    return render(request, "posts/nuevo.html", {"form": form})
