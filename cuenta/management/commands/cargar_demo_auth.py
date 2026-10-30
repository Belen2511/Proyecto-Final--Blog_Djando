from decouple import config
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from posts.models import Post

User = get_user_model()

# Se puede cambiar con DEMO_PASSWORD en el .env (conviene hacerlo si el sitio es público).
CLAVE_DEMO = config("DEMO_PASSWORD", default="clave-demo-123")


class Command(BaseCommand):
    help = "Crea usuarios demo (ana, beto, carla, dani), los grupos Editores y Publicadores y 2 posts."

    def handle(self, *args, **options):
        # Editores: pueden editar/eliminar posts ajenos (permisos globales change/delete).
        editores, _ = Group.objects.get_or_create(name="Editores")
        editores.permissions.set(
            Permission.objects.filter(content_type__app_label="posts",
                                      codename__in=["change_post", "delete_post"])
        )
        # Publicadores: tienen el permiso propio del Meta del modelo.
        publicadores, _ = Group.objects.get_or_create(name="Publicadores")
        publicadores.permissions.set(
            Permission.objects.filter(content_type__app_label="posts", codename="puede_publicar")
        )

        usuarios = {}
        for nombre in ("ana", "beto", "carla", "dani"):
            user, creado = User.objects.get_or_create(username=nombre, defaults={"email": f"{nombre}@ejemplo.com"})
            if creado:
                user.set_password(CLAVE_DEMO)  # set_password hashea; nunca guardar texto plano
                user.save()
            usuarios[nombre] = user
        usuarios["carla"].groups.add(editores)
        usuarios["dani"].groups.add(publicadores)

        # Por el ORM se puede crear con cualquier estado; por el formulario, publicar exige el permiso.
        Post.objects.get_or_create(titulo="Hola desde Ana", autor=usuarios["ana"], defaults={
            "contenido": "Primer post de Ana.", "estado": Post.PUBLICADO, "likes": 5})
        Post.objects.get_or_create(titulo="Mi post borrador", autor=usuarios["beto"], defaults={
            "contenido": "Beto escribe.", "estado": Post.BORRADOR})

        self.stdout.write(self.style.SUCCESS(
            "Listo. ana y beto: autores comunes. carla: Editores. dani: Publicadores. "
            + ("Contraseña de todos: clave-demo-123" if CLAVE_DEMO == "clave-demo-123"
               else "Contraseña de todos: la de DEMO_PASSWORD")))
