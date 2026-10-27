from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Perfil

User = get_user_model()


class RegistroForm(UserCreationForm):
    """UserCreationForm ya trae username + password1 + password2 con validación.
    Le sumamos el email."""

    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe un usuario con ese correo.")
        return email
    
    


class UsuarioForm(forms.ModelForm):
    """Datos propios del User que se pueden editar desde el perfil."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        labels = {"first_name": "Nombre", "last_name": "Apellido", "email": "Correo electrónico"}


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ("biografia", "link_web", "avatar")
        labels = {"biografia": "Biografía", "link_web": "Sitio web", "avatar": "Avatar"}
        widgets = {"biografia": forms.Textarea(attrs={"rows": 4})}
