import shutil
import tempfile

from django.contrib.auth.models import User
from django.core import mail
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

    def test_admin_muestra_el_perfil_al_editar_un_usuario(self):
        admin = User.objects.create_superuser("admin2", "admin2@test.com", "x")
        self.client.force_login(admin)
        r = self.client.get(reverse("admin:auth_user_change", args=[admin.pk]))
        self.assertContains(r, "perfil-TOTAL_FORMS")
        r = self.client.get(reverse("admin:auth_user_add"))
        self.assertNotContains(r, "perfil-TOTAL_FORMS")

    def test_migracion_crea_perfiles_faltantes(self):
        import importlib
        from django.apps import apps
        migracion = importlib.import_module("cuenta.migrations.0002_crear_perfiles_faltantes")
        viejo = User.objects.create_user("hugo", password="x")
        Perfil.objects.filter(user=viejo).delete()  # simula un usuario de antes del modelo
        migracion.crear_perfiles_faltantes(apps, None)
        self.assertTrue(Perfil.objects.filter(user=viejo).exists())

    def test_usuario_sin_perfil_puede_ver_su_perfil(self):
        user = User.objects.create_user("ines", password="x")
        Perfil.objects.filter(user=user).delete()
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("perfil")).status_code, 200)
        self.assertTrue(Perfil.objects.filter(user=user).exists())


class SenalPerfilTests(TestCase):
    def test_el_perfil_nace_solo(self):
        user = User.objects.create_user("juan", "juan@test.com", "x")
        self.assertTrue(Perfil.objects.filter(user=user).exists())  # lo creó la señal

    def test_superusuario_tambien_tiene_perfil(self):
        admin = User.objects.create_superuser("jefa", "jefa@test.com", "x")
        self.assertTrue(Perfil.objects.filter(user=admin).exists())

    def test_guardar_de_nuevo_no_duplica_el_perfil(self):
        user = User.objects.create_user("kari", password="x")
        user.first_name = "Kari"
        user.save()
        self.assertEqual(Perfil.objects.filter(user=user).count(), 1)


class PerfilPublicoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("lola", "lola@test.com", "x")
        Post.objects.create(titulo="Post visible", autor=cls.user, estado=Post.PUBLICADO)
        Post.objects.create(titulo="Post oculto", autor=cls.user, estado=Post.BORRADOR)

    def test_muestra_usuario_y_solo_posts_publicados(self):
        r = self.client.get(reverse("perfil_publico", args=["lola"]))
        self.assertContains(r, "@lola")
        self.assertContains(r, "Post visible")
        self.assertNotContains(r, "Post oculto")

    def test_usuario_inexistente_da_404(self):
        r = self.client.get(reverse("perfil_publico", args=["nadie"]))
        self.assertEqual(r.status_code, 404)

    def test_link_de_editar_solo_para_el_duenio(self):
        url = reverse("perfil_publico", args=["lola"])
        self.assertNotContains(self.client.get(url), reverse("editar_perfil"))
        self.client.force_login(self.user)
        self.assertContains(self.client.get(url), reverse("editar_perfil"))

    def test_detalle_enlaza_al_perfil_del_autor(self):
        post = Post.objects.get(titulo="Post visible")
        r = self.client.get(reverse("detalle_post", args=[post.slug]))
        self.assertContains(r, reverse("perfil_publico", args=["lola"]))


class PasswordTests(TestCase):
    CLAVE = "ClaveSegura123!"
    NUEVA = "OtraClave456!"

    def setUp(self):
        self.user = User.objects.create_user("mora", "mora@test.com", self.CLAVE)

    def test_cambiar_password_requiere_login(self):
        url = reverse("password_change")
        self.assertRedirects(self.client.get(url), f"{reverse('Login')}?next={url}")

    def test_cambiar_password(self):
        self.client.force_login(self.user)
        r = self.client.post(reverse("password_change"), {
            "old_password": self.CLAVE, "new_password1": self.NUEVA, "new_password2": self.NUEVA,
        })
        self.assertRedirects(r, reverse("password_change_done"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.NUEVA))

    def test_recuperar_password_por_mail(self):
        r = self.client.post(reverse("password_reset"), {"email": "mora@test.com"})
        self.assertRedirects(r, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        enlace = next(l for l in mail.outbox[0].body.splitlines() if "/cuenta/password/reset/" in l)
        ruta = enlace.split("testserver", 1)[1].strip()
        r = self.client.get(ruta, follow=True)  # Django redirige a una URL con token de sesión
        self.assertContains(r, "Elegí una contraseña nueva")
        r = self.client.post(r.redirect_chain[-1][0], {"new_password1": self.NUEVA, "new_password2": self.NUEVA})
        self.assertRedirects(r, reverse("password_reset_complete"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.NUEVA))


class MisPostsTests(TestCase):
    def test_mis_posts_muestra_los_posts_del_usuario(self):
        user = User.objects.create_user("nico", password="x")
        Post.objects.create(titulo="Lo que escribí", autor=user)
        self.client.force_login(user)
        self.assertContains(self.client.get(reverse("mis_posts")), "Lo que escribí")
