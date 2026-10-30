"""Tests de 'más formas de proteger vistas': mixins, decoradores, permiso propio y guardian."""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse
from guardian.shortcuts import assign_perm

from .forms import PostForm
from .models import Post
from .views import puede_modificar

User = get_user_model()
CLAVE = "clave-test-123"


def permisos(*codenames):
    return Permission.objects.filter(content_type__app_label="posts", codename__in=codenames)


class ProteccionTestCase(TestCase):
    """ana y beto: autores comunes. carla: Editores (permisos globales). dani: Publicadores."""

    @classmethod
    def setUpTestData(cls):
        cls.ana = User.objects.create_user("ana", password=CLAVE)
        cls.beto = User.objects.create_user("beto", password=CLAVE)
        cls.carla = User.objects.create_user("carla", password=CLAVE)
        cls.dani = User.objects.create_user("dani", password=CLAVE)
        editores = Group.objects.create(name="Editores")
        editores.permissions.set(permisos("change_post", "delete_post"))
        cls.carla.groups.add(editores)
        publicadores = Group.objects.create(name="Publicadores")
        publicadores.permissions.set(permisos("puede_publicar"))
        cls.dani.groups.add(publicadores)

    def crear(self, autor=None, **extra):
        datos = {"titulo": "Post de prueba", "contenido": "Hola", "estado": "publicado",
                 "autor": autor or self.ana}
        datos.update(extra)
        return Post.objects.create(**datos)

    def entrar(self, nombre):
        self.client.login(username=nombre, password=CLAVE)

    def login_url(self, destino):
        return f"{reverse('Login')}?next={destino}"


class MixinsTests(ProteccionTestCase):
    def test_login_required_mixin(self):
        url = reverse("cbv_crear_post")
        self.assertRedirects(self.client.get(url), self.login_url(url))

    def test_crear_con_clase_asigna_autor(self):
        self.entrar("ana")
        r = self.client.post(reverse("cbv_crear_post"),
                             {"titulo": "Desde la clase", "contenido": "x", "estado": "borrador"})
        post = Post.objects.get(titulo="Desde la clase")
        self.assertRedirects(r, post.get_absolute_url())
        self.assertEqual(post.autor, self.ana)

    def test_editar_anonimo_va_al_login(self):
        p = self.crear()
        url = reverse("cbv_editar_post", args=[p.slug])
        self.assertRedirects(self.client.get(url), self.login_url(url))

    def test_user_passes_test_mixin_solo_el_dueno(self):
        p = self.crear(autor=self.ana)
        url = reverse("cbv_editar_post", args=[p.slug])
        self.entrar("beto")
        self.assertEqual(self.client.get(url).status_code, 403)
        self.client.logout()
        self.entrar("ana")
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_editar_con_clase_guarda(self):
        p = self.crear(autor=self.ana)
        self.entrar("ana")
        r = self.client.post(reverse("cbv_editar_post", args=[p.slug]),
                             {"titulo": "Título nuevo", "contenido": "y", "estado": "publicado"})
        self.assertRedirects(r, p.get_absolute_url())
        p.refresh_from_db()
        self.assertEqual(p.titulo, "Título nuevo")

    def test_editor_global_tambien_pasa_el_test_func(self):
        p = self.crear(autor=self.ana)
        self.entrar("carla")
        self.assertEqual(self.client.get(reverse("cbv_editar_post", args=[p.slug])).status_code, 200)

    def test_eliminar_con_clase(self):
        p = self.crear(autor=self.ana)
        url = reverse("cbv_eliminar_post", args=[p.slug])
        self.entrar("beto")
        self.assertEqual(self.client.post(url).status_code, 403)
        self.assertEqual(Post.objects.count(), 1)
        self.client.logout()
        self.entrar("ana")
        self.assertRedirects(self.client.post(url), reverse("lista_posts"))
        self.assertEqual(Post.objects.count(), 0)

    def test_permission_required_mixin(self):
        self.crear(titulo="Un borrador", estado="borrador")
        url = reverse("cbv_borradores")
        self.assertRedirects(self.client.get(url), self.login_url(url))   # anónimo: login
        self.entrar("ana")
        self.assertEqual(self.client.get(url).status_code, 403)           # logueado sin permiso: 403
        self.client.logout()
        self.entrar("carla")
        r = self.client.get(url)
        self.assertContains(r, "Un borrador")


class DecoradoresTests(ProteccionTestCase):
    def test_permission_required_con_raise_exception(self):
        self.crear(titulo="Un borrador", estado="borrador")
        url = reverse("borradores")
        self.assertRedirects(self.client.get(url), self.login_url(url))
        self.entrar("ana")
        self.assertEqual(self.client.get(url).status_code, 403)
        self.client.logout()
        self.entrar("carla")
        self.assertContains(self.client.get(url), "Un borrador")

    def test_borradores_no_muestra_publicados(self):
        self.crear(titulo="Publicado visible", estado="publicado")
        self.entrar("carla")
        self.assertNotContains(self.client.get(reverse("borradores")), "Publicado visible")

    def test_user_passes_test_redirige_al_login_aunque_este_logueado(self):
        url = reverse("panel_editores")
        self.entrar("ana")
        # A diferencia de raise_exception=True, acá NO hay 403: manda al login.
        self.assertRedirects(self.client.get(url), self.login_url(url))
        self.client.logout()
        self.entrar("carla")
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_el_decorador_no_ve_el_objeto(self):
        # es_editor solo recibe al usuario: no distingue entre posts.
        from .views import es_editor
        self.assertTrue(es_editor(self.carla))
        self.assertFalse(es_editor(self.ana))


class PermisoPropioTests(ProteccionTestCase):
    def datos(self, **extra):
        base = {"titulo": "Post para publicar", "contenido": "x", "estado": "publicado"}
        base.update(extra)
        return base

    def test_el_permiso_existe(self):
        self.assertTrue(Permission.objects.filter(codename="puede_publicar").exists())

    def test_sin_permiso_no_puede_publicar(self):
        self.entrar("ana")
        r = self.client.post(reverse("nuevo_post"), self.datos())
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "No tenés permiso para publicar")
        self.assertEqual(Post.objects.count(), 0)

    def test_sin_permiso_si_puede_guardar_borrador(self):
        self.entrar("ana")
        self.client.post(reverse("nuevo_post"), self.datos(estado="borrador"))
        self.assertEqual(Post.objects.get().estado, "borrador")

    def test_con_permiso_publica(self):
        self.entrar("dani")
        self.client.post(reverse("nuevo_post"), self.datos())
        self.assertEqual(Post.objects.get().estado, "publicado")

    def test_tambien_vale_en_la_vista_con_clase(self):
        self.entrar("ana")
        r = self.client.post(reverse("cbv_crear_post"), self.datos())
        self.assertContains(r, "No tenés permiso para publicar")
        self.assertEqual(Post.objects.count(), 0)

    def test_editar_un_post_ya_publicado_sin_cambiar_el_estado_pasa(self):
        p = self.crear(autor=self.ana, estado="publicado")
        self.entrar("ana")
        r = self.client.post(reverse("editar_post", args=[p.slug]), self.datos(titulo="Título corregido"))
        self.assertRedirects(r, p.get_absolute_url())
        p.refresh_from_db()
        self.assertEqual((p.titulo, p.estado), ("Título corregido", "publicado"))

    def test_pasar_un_borrador_a_publicado_exige_el_permiso(self):
        p = self.crear(autor=self.ana, estado="borrador")
        self.entrar("ana")
        r = self.client.post(reverse("editar_post", args=[p.slug]), self.datos())
        self.assertContains(r, "No tenés permiso para publicar")
        p.refresh_from_db()
        self.assertEqual(p.estado, "borrador")

    def test_form_sin_usuario_no_puede_publicar(self):
        form = PostForm(self.datos())
        self.assertFalse(form.is_valid())
        self.assertIn("estado", form.errors)

    def test_permiso_dado_directo_al_usuario(self):
        self.ana.user_permissions.add(*permisos("puede_publicar"))
        ana = User.objects.get(pk=self.ana.pk)      # releer: Django cachea los permisos en el objeto
        self.assertTrue(ana.has_perm("posts.puede_publicar"))


class GuardianTests(ProteccionTestCase):
    def test_permiso_por_objeto_no_es_global(self):
        p = self.crear(autor=self.ana)
        self.assertFalse(self.beto.has_perm("posts.change_post", p))
        assign_perm("change_post", self.beto, p)
        beto = User.objects.get(pk=self.beto.pk)
        self.assertTrue(beto.has_perm("posts.change_post", p))
        self.assertFalse(beto.has_perm("posts.change_post"))     # el global sigue en False

    def test_permiso_global_no_implica_el_de_objeto(self):
        p = self.crear(autor=self.ana)
        self.assertTrue(self.carla.has_perm("posts.change_post"))
        self.assertFalse(self.carla.has_perm("posts.change_post", p))
        self.assertTrue(puede_modificar(self.carla, p))           # por eso puede_modificar mira los dos

    def test_compartir_habilita_a_editar_solo_ese_post(self):
        p1 = self.crear(titulo="Post uno", autor=self.ana)
        p2 = self.crear(titulo="Post dos", autor=self.ana)
        self.entrar("ana")
        r = self.client.post(reverse("compartir_post", args=[p1.slug]), {"usuario": "beto"})
        self.assertRedirects(r, reverse("compartir_post", args=[p1.slug]))
        self.client.logout()
        self.entrar("beto")
        self.assertEqual(self.client.get(reverse("editar_post", args=[p1.slug])).status_code, 200)
        self.assertEqual(self.client.get(reverse("editar_post", args=[p2.slug])).status_code, 403)

    def test_compartidos_conmigo(self):
        p1 = self.crear(titulo="Compartido con beto", autor=self.ana)
        self.crear(titulo="Privado de ana", autor=self.ana)
        assign_perm("change_post", self.beto, p1)
        self.entrar("beto")
        r = self.client.get(reverse("mis_posts"))
        self.assertContains(r, "Compartido con beto")
        self.assertNotContains(r, "Privado de ana")

    def test_un_editor_global_no_ve_todo_como_compartido(self):
        self.crear(titulo="Post ajeno", autor=self.ana)
        self.entrar("carla")
        self.assertNotContains(self.client.get(reverse("mis_posts")), "Post ajeno")

    def test_solo_la_autora_comparte(self):
        p = self.crear(autor=self.ana)
        assign_perm("change_post", self.beto, p)
        self.entrar("beto")                                       # colaborador, no autor
        self.assertEqual(self.client.get(reverse("compartir_post", args=[p.slug])).status_code, 403)
        self.client.logout()
        self.assertRedirects(self.client.get(reverse("compartir_post", args=[p.slug])),
                             self.login_url(reverse("compartir_post", args=[p.slug])))

    def test_quitar_colaborador(self):
        p = self.crear(autor=self.ana)
        assign_perm("change_post", self.beto, p)
        url = reverse("quitar_colaborador", args=[p.slug, "beto"])
        self.entrar("ana")
        self.assertEqual(self.client.get(url).status_code, 405)   # solo POST
        self.client.post(url)
        self.client.logout()
        self.entrar("beto")
        self.assertEqual(self.client.get(reverse("editar_post", args=[p.slug])).status_code, 403)

    def test_compartir_valida_el_usuario(self):
        p = self.crear(autor=self.ana)
        self.entrar("ana")
        url = reverse("compartir_post", args=[p.slug])
        self.assertContains(self.client.post(url, {"usuario": "nadie"}), "No existe ese usuario")
        self.assertContains(self.client.post(url, {"usuario": "AnonymousUser"}), "No existe ese usuario")
        self.assertContains(self.client.post(url, {"usuario": "ana"}), "ya es la autora")

    def test_menu_borradores_segun_permiso(self):
        self.entrar("ana")
        self.assertNotContains(self.client.get(reverse("lista_posts")), "/borradores/")
        self.client.logout()
        self.entrar("carla")
        self.assertContains(self.client.get(reverse("lista_posts")), "/borradores/")


class DemoYPaginasTests(ProteccionTestCase):
    def test_comando_cargar_demo_auth(self):
        from django.core.management import call_command
        from io import StringIO
        call_command("cargar_demo_auth", stdout=StringIO())
        carla = User.objects.get(username="carla")
        self.assertTrue(carla.groups.filter(name="Editores").exists())
        self.assertTrue(User.objects.get(username="dani").has_perm("posts.puede_publicar"))
        self.assertTrue(Post.objects.filter(titulo="Hola desde Ana").exists())
        call_command("cargar_demo_auth", stdout=StringIO())  # correrlo dos veces no duplica nada
        self.assertEqual(Post.objects.filter(titulo="Hola desde Ana").count(), 1)

    def test_pagina_403_propia(self):
        self.entrar("ana")
        r = self.client.get(reverse("borradores"))
        self.assertEqual(r.status_code, 403)
        self.assertContains(r, "No tenés permiso para ver esta página", status_code=403)

    def test_registro_inicia_sesion_con_dos_backends(self):
        self.client.post(reverse("registro"), {
            "username": "nuevo", "email": "nuevo@test.com",
            "password1": "ClaveSegura123!", "password2": "ClaveSegura123!",
        })
        self.assertEqual(int(self.client.session["_auth_user_id"]), User.objects.get(username="nuevo").pk)
