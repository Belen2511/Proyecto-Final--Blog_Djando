from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RegistroForm


def registro(request):
    if request.user.is_authenticated:
        return redirect("lista_posts")
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()   
            login(request, user) 
            messages.success(request, f"¡Bienvenido, {user.username}!")
            return redirect("lista_posts")
    else:
        form = RegistroForm()
    return render(request, "cuentas/registro.html", {"form": form})

# Create your views here.
