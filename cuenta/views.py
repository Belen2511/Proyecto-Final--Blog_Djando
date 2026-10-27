from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import PerfilForm, RegistroForm, UsuarioForm
from .models import Perfil


def registro(request):
    if request.user.is_authenticated:
        return redirect("lista_posts")
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            Perfil.objects.create(user=usuario)  # el perfil se crea acá, sin signals
            login(request, usuario)
            messages.success(request, f"¡Bienvenido, {usuario.username}!")
            return redirect("perfil")
    else:
        form = RegistroForm()
    return render(request, "cuentas/registro.html", {"form": form})


@login_required
def perfil(request):
    # get_or_create cubre usuarios creados antes del modelo Perfil (o desde el admin)
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
