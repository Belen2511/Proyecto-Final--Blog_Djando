from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Perfil

User = get_user_model()


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("user", "link_web")
    search_fields = ("user__username", "user__email")


class PerfilInline(admin.StackedInline):
    """Permite ver y editar el perfil desde la ficha del usuario en el admin."""

    model = Perfil
    can_delete = False
    extra = 0


class UsuarioConPerfilAdmin(UserAdmin):
    inlines = [PerfilInline]

    def get_inlines(self, request, obj=None):
        # Al crear un usuario no se muestra: la señal crea el perfil sola.
        # Se edita después, desde la ficha del usuario.
        return self.inlines if obj else []


admin.site.unregister(User)
admin.site.register(User, UsuarioConPerfilAdmin)
