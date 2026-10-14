from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "autor", "contenido", "likes"]


class BuscarForm(forms.Form):
    q = forms.CharField(label="Título", required=False)
    autor = forms.CharField(label="Autor", required=False)


class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    mensaje = forms.CharField(widget=forms.Textarea)
