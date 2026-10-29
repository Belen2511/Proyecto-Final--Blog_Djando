import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from posts.models import Post

from .models import Perfil

# GIF de 1x1 píxel para probar la subida del avatar
GIF = (b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04"
       b"\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;")
MEDIA_TMP = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_TMP)
class FlujoUsuarioTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_TMP, ignore_errors=True)
        super().tearDownClass()

    def test_registro_crea_usuario_y_perfil(self):
        r = self.client.post(reverse("registro"), {
            "username": "ana", "email": "ana@test.com",
            "password1": "ClaveSegura123!", "password2": "ClaveSegura123!",
        })
        self.assertRedirects(r, reverse("perfil"))
        self.assertTrue(Perfil.objects.filter(user__username="ana").exists())

    def test_login_y_logout(self):
        User.objects.create_user("beto", password="ClaveSegura123!")
        r = self.client.post(reverse("Login"), {"username": "beto", "password": "ClaveSegura123!"})
        self.assertRedirects(r, reverse("lista_posts"))
        r = self.client.post(reverse("Logout"))
        self.assertRedirects(r, reverse("lista_posts"))

    def test_rutas_protegidas_redirigen_al_login(self):
        autor = User.objects.create_user("carla", password="x")
        post = Post.objects.create(titulo="Hola", autor=autor)
        for url in [reverse("nuevo_post"), reverse("editar_post", args=[post.slug]),
                    reverse("eliminar_post", args=[post.slug]), reverse("perfil"),
                    reverse("editar_perfil")]:
            r = self.client.get(url)
            self.assertRedirects(r, f"{reverse('Login')}?next={url}", msg_prefix=url)

    def test_listado_y_detalle_son_publicos(self):
        autor = User.objects.create_user("dani", password="x")
        post = Post.objects.create(titulo="Público", autor=autor)
        self.assertEqual(self.client.get(reverse("lista_posts")).status_code, 200)
        self.assertEqual(self.client.get(reverse("detalle_post", args=[post.slug])).status_code, 200)

    def test_editar_perfil_con_avatar(self):
        user = User.objects.create_user("eva", password="x")
        self.client.force_login(user)
        r = self.client.post(reverse("editar_perfil"), {
            "first_name": "Eva", "last_name": "P", "email": "eva@test.com",
            "biografia": "Me gusta escribir", "link_web": "",
            "avatar": SimpleUploadedFile("a.gif", GIF, content_type="image/gif"),
        })
        self.assertRedirects(r, reverse("perfil"))
        perfil = Perfil.objects.get(user=user)
        self.assertEqual(perfil.biografia, "Me gusta escribir")
        self.assertTrue(perfil.avatar.name.startswith("avatares/"))
        pagina = self.client.get(reverse("perfil"))
        self.assertContains(pagina, perfil.avatar.url)
        self.assertContains(pagina, "Mi perfil")

    def test_crud_posts_logueado(self):
        user = User.objects.create_user("fede", password="x")
        self.client.force_login(user)
        r = self.client.post(reverse("nuevo_post"), {"titulo": "Mi post", "contenido": "c", "estado": "publicado"})
        post = Post.objects.get(titulo="Mi post")
        self.assertRedirects(r, reverse("detalle_post", args=[post.slug]))
        self.client.post(reverse("editar_post", args=[post.slug]), {"titulo": "Editado", "contenido": "c", "estado": "publicado"})
        post.refresh_from_db()
        self.assertEqual(post.titulo, "Editado")
        self.client.post(reverse("eliminar_post", args=[post.slug]))
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())


class PerfilCasosLimiteTests(TestCase):
    """Ningún usuario debería quedar sin perfil."""

    def test_usuario_creado_desde_el_admin_tiene_perfil(self):
        admin = User.objects.create_superuser("admin", "admin@test.com", "x")
        self.client.force_login(admin)
        self.client.post(reverse("admin:auth_user_add"), {
            "username": "gaby", "password1": "ClaveSegura123!", "password2": "ClaveSegura123!",
            "usable_password": "true",
            "perfil-TOTAL_FORMS": "0", "perfil-INITIAL_FORMS": "0",
            "perfil-MIN_NUM_FORMS": "0", "perfil-MAX_NUM_FORMS": "1",
        })
        self.assertTrue(Perfil.objects.filter(user__username="gaby").exists())

    def test_migracion_crea_perfiles_faltantes(self):
        import importlib
        from django.apps import apps
        migracion = importlib.import_module("cuenta.migrations.0002_crear_perfiles_faltantes")
        viejo = User.objects.create_user("hugo", password="x")  # usuario sin perfil
        migracion.crear_perfiles_faltantes(apps, None)
        self.assertTrue(Perfil.objects.filter(user=viejo).exists())

    def test_usuario_sin_perfil_puede_ver_su_perfil(self):
        user = User.objects.create_user("ines", password="x")
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("perfil")).status_code, 200)
        self.assertTrue(Perfil.objects.filter(user=user).exists())
