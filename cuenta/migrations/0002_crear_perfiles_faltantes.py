from django.conf import settings
from django.db import migrations


def crear_perfiles_faltantes(apps, schema_editor):
    """Crea un perfil vacío para los usuarios que existían antes del modelo Perfil."""
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(app_label, model_name)
    Perfil = apps.get_model("cuenta", "Perfil")
    sin_perfil = User.objects.filter(perfil__isnull=True)
    Perfil.objects.bulk_create([Perfil(user=u) for u in sin_perfil])


class Migration(migrations.Migration):

    dependencies = [
        ("cuenta", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(crear_perfiles_faltantes, migrations.RunPython.noop),
    ]
