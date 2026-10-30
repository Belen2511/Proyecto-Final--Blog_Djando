from django import forms
from django.contrib.auth import get_user_model
from guardian.conf import settings as guardian_settings

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "contenido", "estado", "imagen"]

    def __init__(self, *args, user=None, **kwargs):
        # La vista le pasa el usuario para poder preguntar por sus permisos.
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_estado(self):
        estado = self.cleaned_data["estado"]
        # Solo se bloquea el cambio A "publicado": si el post ya estaba publicado y no se toca, pasa.
        publica_ahora = estado == Post.PUBLICADO and estado != self.instance.estado
        if publica_ahora and not (self.user and self.user.has_perm("posts.puede_publicar")):
            raise forms.ValidationError("No tenés permiso para publicar. Guardalo como borrador.")
        return estado


class BuscarForm(forms.Form):
    q = forms.CharField(label="Título", required=False)
    autor = forms.CharField(label="Autor", required=False)


class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    mensaje = forms.CharField(widget=forms.Textarea)


class CompartirForm(forms.Form):
    """Para darle a otro usuario permiso de editar UN post (permiso por objeto, django-guardian)."""

    usuario = forms.CharField(label="Nombre de usuario con quien compartir")

    def __init__(self, *args, post=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.post = post

    def clean_usuario(self):
        username = self.cleaned_data["usuario"].strip()
        User = get_user_model()
        try:
            usuario = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("No existe ese usuario.")
        if usuario.username == guardian_settings.ANONYMOUS_USER_NAME:
            raise forms.ValidationError("No existe ese usuario.")
        if usuario.id == self.post.autor_id:
            raise forms.ValidationError("Esa persona ya es la autora del post.")
        return usuario  # devuelve el objeto User, no el texto
