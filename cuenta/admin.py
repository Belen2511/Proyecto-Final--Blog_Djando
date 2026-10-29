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

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # Si el usuario se creó desde el admin sin completar el perfil, se lo creamos vacío
        Perfil.objects.get_or_create(user=form.instance)


admin.site.unregister(User)
admin.site.register(User, UsuarioConPerfilAdmin)
