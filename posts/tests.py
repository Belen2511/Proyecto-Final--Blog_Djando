import shutil
import tempfile

from django.contrib.auth.models import Group, Permission, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Post

# GIF de 1x1 píxel para probar la carga de imágenes
GIF = (b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04"
       b"\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;")
MEDIA_TMP = tempfile.mkdtemp()


def imagen(nombre="foto.gif"):
    return SimpleUploadedFile(nombre, GIF, content_type="image/gif")


@override_settings(MEDIA_ROOT=MEDIA_TMP)
class CrudConImagenesTests(TestCase):
    """CRUD de posts desde la interfaz web, con imágenes."""

    @classmethod
    def setUpTestData(cls):
        cls.autora = User.objects.create_user("vera", password="x")
        publicadores = Group.objects.create(name="Publicadores")
        publicadores.permissions.set(Permission.objects.filter(codename="puede_publicar"))
        cls.autora.groups.add(publicadores)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_TMP, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.client.force_login(self.autora)

    def crear(self, **extra):
        datos = {"titulo": "Post con foto", "contenido": "Texto", "estado": "publicado", "imagen": imagen()}
        datos.update(extra)
        return self.client.post(reverse("nuevo_post"), datos)

    def test_crear_post_con_imagen(self):
        r = self.crear()
        post = Post.objects.get(titulo="Post con foto")
        self.assertRedirects(r, reverse("detalle_post", args=[post.slug]))
        self.assertTrue(post.imagen.name.startswith("posts/"))
        self.assertEqual(post.autor, self.autora)

    def test_la_imagen_se_muestra_en_detalle_y_listado(self):
        self.crear()
        post = Post.objects.get(titulo="Post con foto")
        self.assertContains(self.client.get(reverse("detalle_post", args=[post.slug])), post.imagen.url)
        self.assertContains(self.client.get(reverse("lista_posts")), post.imagen.url)

    def test_post_sin_imagen_se_muestra_sin_errores(self):
        self.client.post(reverse("nuevo_post"), {"titulo": "Sin foto", "contenido": "x", "estado": "publicado"})
        post = Post.objects.get(titulo="Sin foto")
        self.assertFalse(post.imagen)
        self.assertContains(self.client.get(reverse("detalle_post", args=[post.slug])), "Este post no tiene imagen")

    def test_editar_cambia_la_imagen(self):
        self.crear()
        post = Post.objects.get(titulo="Post con foto")
        self.client.post(reverse("editar_post", args=[post.slug]), {
            "titulo": "Post con foto", "contenido": "Texto", "estado": "publicado", "imagen": imagen("otra.gif"),
        })
        post.refresh_from_db()
        self.assertIn("otra", post.imagen.name)

    def test_eliminar_post(self):
        self.crear()
        post = Post.objects.get(titulo="Post con foto")
        r = self.client.post(reverse("eliminar_post", args=[post.slug]))
        self.assertRedirects(r, reverse("lista_posts"))
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

    def test_archivo_que_no_es_imagen_se_rechaza(self):
        r = self.crear(imagen=SimpleUploadedFile("nota.txt", b"hola", content_type="text/plain"))
        self.assertEqual(r.status_code, 200)
        self.assertFalse(Post.objects.filter(titulo="Post con foto").exists())
