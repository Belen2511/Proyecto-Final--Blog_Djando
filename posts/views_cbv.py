"""Las mismas reglas que en views.py, pero con vistas basadas en clases y mixins.

Regla de oro: los mixins van ANTES de la vista genérica en la lista de herencia.
Si se ponen después, no protegen y Django no avisa."""
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import PostForm
from .models import Post
from .views import puede_modificar


class PostFormUsuarioMixin:
    """Le pasa request.user al PostForm (lo usa clean_estado para el permiso puede_publicar)."""

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, PostFormUsuarioMixin, CreateView):
    """LoginRequiredMixin = @login_required."""
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    extra_context = {"titulo_pagina": "Crear post (vista con clase)", "texto_boton": "Crear"}
    success_message = "Post creado."

    def form_valid(self, form):
        form.instance.autor = self.request.user  # equivalente a commit=False + post.autor = ...
        return super().form_valid(form)          # redirige a Post.get_absolute_url()


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, PostFormUsuarioMixin, UpdateView):
    """UserPassesTestMixin: la regla vive en test_func y SÍ ve el objeto."""
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    extra_context = {"titulo_pagina": "Editar post (vista con clase)", "texto_boton": "Guardar cambios"}
    success_message = "Cambios guardados."

    def test_func(self):
        return puede_modificar(self.request.user, self.get_object())


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"
    context_object_name = "post"
    success_url = reverse_lazy("lista_posts")
    success_message = "Post eliminado."

    def test_func(self):
        return puede_modificar(self.request.user, self.get_object())


class BorradoresCbvView(PermissionRequiredMixin, ListView):
    """PermissionRequiredMixin = @permission_required. Con usuario logueado y sin permiso => 403."""
    permission_required = "posts.change_post"  # puede ser una lista: se exigen todos
    queryset = Post.objects.filter(estado=Post.BORRADOR).select_related("autor")
    template_name = "posts/lista_protegida.html"
    context_object_name = "posts"
    extra_context = {"titulo": "Borradores (vista con clase)", "mecanismo": "PermissionRequiredMixin"}
