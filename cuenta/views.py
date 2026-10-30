from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from posts.models import Post

from .forms import PerfilForm, RegistroForm, UsuarioForm
from .models import Perfil

User = get_user_model()


def registro(request):
    if request.user.is_authenticated:
        return redirect("lista_posts")
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            # La señal post_save (cuenta/signals.py) crea el perfil al guardar el usuario.
            # atomic: si falla la creación del perfil, tampoco se guarda el usuario.
            with transaction.atomic():
                usuario = form.save()
            # Con dos backends (ModelBackend + guardian), login() necesita saber cuál usar.
            login(request, usuario, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(request, f"¡Bienvenido, {usuario.username}!")
            return redirect("perfil")
    else:
        form = RegistroForm()
    return render(request, "cuentas/registro.html", {"form": form})


def perfil_publico(request, username):
    """Página pública de un usuario: sus datos y sus posts publicados."""
    usuario = get_object_or_404(User, username=username)
    perfil, _ = Perfil.objects.get_or_create(user=usuario)
    posts = usuario.posts.filter(estado=Post.PUBLICADO)
    return render(request, "cuentas/perfil_publico.html", {
        "usuario": usuario, "perfil": perfil, "posts": posts,
    })


@login_required
def perfil(request):
    # get_or_create: red de seguridad por si algún usuario quedó sin perfil
    perfil, _ = Perfil.objects.get_or_create(user=request.user)
    return render(request, "cuentas/perfil.html", {"perfil": perfil})


@login_required
def editar_perfil(request):
    perfil, _ = Perfil.objects.get_or_create(user=request.user)
    if request.method == "POST":
        usuario_form = UsuarioForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)  # FILES => avatar
        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()
            perfil_form.save()
            messages.success(request, "Perfil actualizado.")
            return redirect("perfil")
    else:
        usuario_form = UsuarioForm(instance=request.user)
        perfil_form = PerfilForm(instance=perfil)
    return render(request, "cuentas/editar_perfil.html", {
        "usuario_form": usuario_form,
        "perfil_form": perfil_form,
    })
