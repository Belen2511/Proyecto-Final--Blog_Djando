# Blog Django

Proyecto base de un blog web desarrollado con Django.

## Descripción

Este repositorio contiene la estructura inicial de un proyecto Django para construir un blog.
Incluye la configuración base del proyecto (`Config`) y dos aplicaciones: `posts` (publicaciones) y `cuenta` (usuarios y perfiles).

Configuración regional:

- Idioma: `es-ar`
- Zona horaria: `America/Argentina/Buenos_Aires`

## Requisitos

- Python 3.12 o superior
- Git

## Instalación

Clonar el repositorio:

```bash
gh repo clone Belen2511/Proyecto-Final--Blog_Djando
```

Entrar a la carpeta del proyecto:

```bash
cd Proyecto-Final--Blog_Djando
```

Crear el entorno virtual:

```bash
python -m venv venv
```

Activar el entorno virtual:

En Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

En Linux o macOS:

```bash
source venv/bin/activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Crear el archivo `.env` a partir del ejemplo:

En Windows PowerShell:

```bash
copy .env.example .env
```

En Linux o macOS:

```bash
cp .env.example .env
```

Después abrir `.env` y reemplazar `colocar-una-clave-secreta` por una clave propia.
Se puede generar una con:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

(ver [Configuración segura](#configuración-segura)).

Crear la base de datos (aplica las migraciones de `posts` y `cuenta`):

```bash
python manage.py migrate
```

La base de datos (`db.sqlite3`) no se sube al repositorio, así que este paso
es necesario la primera vez. Después hay que cargar los posts desde el admin
(ver [Cargar contenido desde el admin](#cargar-contenido-desde-el-admin)).

## Ejecutar el servidor

```bash
python manage.py runserver
```

Abrir en el navegador:

```
http://127.0.0.1:8000/
```

Páginas disponibles:

| Ruta | Descripción |
|------|-------------|
| `/` | Página de inicio |
| `/acerca/` | Acerca de (autor y propósito del sitio) |
| `/posts/` | Listado de publicaciones |
| `/posts/<slug>/` | Detalle de una publicación |
| `/posts/nuevo/` | Crear una publicación |
| `/posts/<slug>/editar/` | Editar una publicación |
| `/posts/<slug>/eliminar/` | Eliminar una publicación (pide confirmación) |
| `/admin/` | Panel de administración |

Para detener el servidor: `Ctrl + C`.

## Estructura

```
blog_django/
│
├── manage.py
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── Config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── posts/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── views_cbv.py
│   ├── test_proteccion.py
│   ├── migrations/
│   │
│   ├── templates/
│   │   ├── 403.html
│   │   └── posts/
│   │       ├── base.html
│   │       ├── inicio.html
│   │       ├── acerca.html
│   │       ├── lista_posts.html
│   │       ├── detalle_post.html
│   │       ├── mis_posts.html
│   │       ├── compartir.html
│   │       ├── lista_protegida.html
│   │       ├── post_form.html
│   │       ├── post_confirm_delete.html
│   │       ├── estadisticas.html
│   │       ├── contacto.html
│   │       └── contacto_exito.html
│   │
│   └── static/
│       └── posts/
│           └── css/
│               └── estilos.css
│
└── cuenta/
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── signals.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    ├── management/commands/cargar_demo_auth.py
    ├── migrations/
    │
    └── templates/
        ├── cuentas/
        │   ├── registro.html
        │   ├── perfil.html
        │   ├── perfil_publico.html
        │   └── editar_perfil.html
        └── registration/
            ├── login.html
            ├── password_change_form.html
            ├── password_change_done.html
            ├── password_reset_form.html
            ├── password_reset_done.html
            ├── password_reset_confirm.html
            ├── password_reset_complete.html
            ├── password_reset_email.txt
            └── password_reset_subject.txt
```

Archivos como `.env`, `venv/`, `db.sqlite3` y `media/` existen solo en cada
computadora y no se suben al repositorio (están en `.gitignore`).

## Configuración segura

Los datos privados no están escritos en `Config/settings.py`: se leen desde un
archivo `.env` con la librería **python-decouple**.

```python
from decouple import Csv, config

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())
```

| Variable | Para qué sirve |
|----------|----------------|
| `SECRET_KEY` | Clave que Django usa para sesiones y protección de formularios. Es obligatoria. |
| `DEBUG` | `True` en desarrollo (muestra errores detallados). En un sitio publicado debería ser `False`. |
| `ALLOWED_HOSTS` | Dominios desde los que se puede acceder al sitio, separados por coma. |
| `CSRF_TRUSTED_ORIGINS` | Solo en producción: la dirección con `https://` del sitio publicado. |

- `.env` tiene los valores reales y **no se sube** a GitHub.
- `.env.example` muestra qué variables hay que completar y **sí se sube**.

### Qué se sube y qué no

| Se sube | No se sube (`.gitignore`) |
|---------|---------------------------|
| Código de `Config/`, `posts/` y `cuenta/` | `venv/` (entorno virtual) |
| Migraciones | `__pycache__/` y `*.pyc` |
| Templates y archivos estáticos | `.env` |
| `requirements.txt`, `README.md`, `.gitignore`, `.env.example` | `db.sqlite3` (se recrea con `migrate`) |
| | `media/` (imágenes subidas localmente) |

### Dependencias

`requirements.txt` incluye **Django**, **Pillow** (para `ImageField`),
**python-decouple** (para leer el `.env`) y **django-guardian** (permisos por objeto). Se actualiza con:

```bash
pip freeze > requirements.txt
```

## Modelo Post

Cada publicación tiene `titulo`, `contenido`, `autor`, `likes`, `fecha_creacion`
y `estado`. El estado puede ser:

| Valor | Se muestra como |
|-------|-----------------|
| `borrador` | Borrador |
| `publicado` | Publicado |
| `archivado` | Archivado |

## Cargar contenido desde el admin

Crear un superusuario (la primera vez):

```bash
python manage.py createsuperuser
```

Iniciar el servidor e ingresar a:

```
http://127.0.0.1:8000/admin/
```

Desde la sección **Posts** se pueden crear, editar y borrar publicaciones.
Conviene cargar al menos 3 posts con distintos datos y estados para probar el listado.

## Consultar posts con el ORM

La view `lista_posts` (en `posts/views.py`) trae los posts desde la base de datos
(ordenados del más reciente al más antiguo, por el `ordering` del modelo) y permite
buscarlos por título y por autor con el formulario `BuscarForm`:

```python
def lista_posts(request):
    posts = Post.objects.select_related("autor").all()  # select_related => JOIN para optimizar consultas
    form = BuscarForm(request.GET or None)  # GET: unbound si no hay parámetros
    if form.is_valid():
        q = form.cleaned_data["q"]
        autor = form.cleaned_data["autor"]
        if q:
            posts = posts.filter(titulo__icontains=q)
        if autor:
            posts = posts.filter(autor__username__icontains=autor)
    return render(request, "posts/lista_posts.html", {"posts": posts, "form": form})
```

- `?q=django` filtra los posts cuyo título contiene "django" (sin distinguir mayúsculas).
- `?autor=ana` filtra por el nombre de usuario del autor.
- El listado no filtra por estado: muestra todos los posts y el estado se ve en cada tarjeta.

## Templates y estilos

Todas las páginas extienden de `posts/base.html` con `{% extends 'posts/base.html' %}`
y rellenan el bloque `{% block content %}`. El CSS se carga desde
`posts/static/posts/css/estilos.css` con `{% static %}`.

En `posts/templates/posts/lista_posts.html` se recorren las publicaciones con un
bucle `{% for post in posts %}` y se muestra de cada una el título, el contenido,
el autor, el estado, la fecha de creación y los likes:

```html
{% for post in posts %}
<a class="card" href="{% url 'detalle_post' post.slug %}">
    <h2>{{ post.titulo }}</h2>
    {% if post.imagen %}<img class="miniatura" src="{{ post.imagen.url }}" alt="{{ post.titulo }}">{% endif %}
    <p>{{ post.contenido|linebreaksbr }}</p>
    <div class="meta">
        por {{ post.autor.username }} — {{ post.get_estado_display }} — {{ post.fecha_creacion|date:"d/m/Y H:i" }} — {{ post.likes }} likes
    </div>
</a>
{% empty %}
<p class="stats">No hay posts que coincidan.</p>
{% endfor %}
```

## Checkpoint: Modelos y Admin configurados

Commit de este checkpoint: `Checkpoint: Modelos y Admin configurados.`

En este punto del proyecto quedó listo:

- El modelo `Post` (`titulo`, `contenido`, `autor`, `likes`, `fecha_creacion`, `estado`) definido en `posts/models.py`, con sus migraciones aplicadas.
- El modelo `Post` registrado en el panel de administración (`posts/admin.py`), desde donde se pueden crear, editar y borrar publicaciones.

## Aplicaciones

- `posts`: publicaciones del blog (CRUD con imágenes).
- `cuenta`: usuarios (registro, login, logout y perfil).

## CRUD de posts con imágenes

### Operaciones CRUD disponibles

| Operación | Ruta | Vista |
|-----------|------|-------|
| Listar | `/posts/` | `lista_posts` |
| Ver detalle | `/posts/<slug>/` | `detalle_post` |
| Crear | `/posts/nuevo/` | `crear_post` |
| Editar | `/posts/<slug>/editar/` | `editar_post` |
| Borrar | `/posts/<slug>/eliminar/` | `eliminar_post` |

Todos los templates (`lista_posts.html`, `detalle_post.html`, `post_form.html`,
`post_confirm_delete.html`) extienden de `posts/base.html`. El formulario es
`PostForm` (`posts/forms.py`, un `ModelForm`) con los campos `titulo`,
`contenido`, `estado` e `imagen`. El autor no se elige en el formulario: la vista
`crear_post` lo asigna con el usuario logueado (`post.autor = request.user`).

### Manejo de imágenes

- **Modelo:** `Post.imagen = models.ImageField(upload_to='posts/', null=True, blank=True)`.
  Es opcional y los archivos se guardan en `media/posts/`.
- **Settings:** `MEDIA_URL = '/media/'` y `MEDIA_ROOT = BASE_DIR / 'media'`.
- **URLs:** en `Config/urls.py` se agrega `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`
  (solo con `DEBUG=True`) para ver las imágenes en desarrollo.
- **Vistas:** crear y editar instancian `PostForm(request.POST, request.FILES, ...)`
  para procesar también el archivo subido.
- **Template del formulario:** `<form method="post" enctype="multipart/form-data">`.
- **Mostrar:** el listado y el detalle muestran la imagen solo si existe
  (`{% if post.imagen %}`); si no, el post se ve igual sin romperse.
- La carpeta `media/` está en `.gitignore`.

### Nueva dependencia

Se instaló **Pillow** (necesaria para `ImageField`) y se agregó a `requirements.txt`:

```bash
pip install Pillow
```

Después de actualizar el modelo hay que aplicar las migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Cómo probar la carga de imágenes

1. Ejecutar `python manage.py runserver`.
2. Ir a `http://127.0.0.1:8000/posts/nuevo/`, completar el formulario y elegir una imagen.
3. Al guardar se redirige al detalle, donde se ve la imagen; también aparece en el listado.
4. Verificar que el archivo quedó en `media/posts/`.
5. Editar el post (`/posts/<slug>/editar/`) y cambiar la imagen.
6. Crear otro post sin imagen y comprobar que se muestra sin errores.
7. Eliminar un post desde `/posts/<slug>/eliminar/`.

## Usuarios, autenticación y perfil (Preentrega 11)

Todo lo relacionado con usuarios está en la app `cuenta` (registrada en
`INSTALLED_APPS`) y usa el sistema de autenticación de Django (`django.contrib.auth`).

### Migraciones

Después de clonar o actualizar el proyecto hay que aplicar las migraciones
(incluyen la tabla del modelo `Perfil`):

```bash
python manage.py makemigrations
python manage.py migrate
```

### Rutas de usuarios

| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/cuenta/registro/` | `registro` | Crear una cuenta nueva |
| `/cuenta/login/` | `LoginView` (nativa) | Iniciar sesión |
| `/cuenta/logout/` | `LogoutView` (nativa) | Cerrar sesión (POST) |
| `/cuenta/perfil/` | `perfil` | Ver mi perfil (requiere login) |
| `/cuenta/perfil/editar/` | `editar_perfil` | Editar mi perfil (requiere login) |
| `/cuenta/perfil/<usuario>/` | `perfil_publico` | Perfil público de un usuario con sus posts publicados |
| `/cuenta/password/cambiar/` | `PasswordChangeView` (nativa) | Cambiar la contraseña (requiere login) |
| `/cuenta/password/recuperar/` | `PasswordResetView` (nativa) | Pedir un mail para recuperar la contraseña |

### Registro

`RegistroForm` (`cuenta/forms.py`) extiende `UserCreationForm` y agrega el campo
`email` (obligatorio y sin repetir). La vista `registro` guarda el usuario dentro
de un `transaction.atomic()` (si falla la creación del perfil, tampoco se guarda
el usuario), inicia la sesión automáticamente y redirige a **Mi perfil**.
El perfil lo crea la señal `post_save` (ver [Señal: el perfil nace solo](#señal-el-perfil-nace-solo)).

### Login y logout

- **Login:** `/cuenta/login/` usa `LoginView` con el template propio
  `cuenta/templates/registration/login.html`, que extiende de `posts/base.html`.
- **Logout:** botón **Cerrar sesión** del menú, que envía un POST a `LogoutView`.
- Redirecciones en `Config/settings.py`:

```python
LOGIN_URL = "Login"
LOGIN_REDIRECT_URL = "lista_posts"
LOGOUT_REDIRECT_URL = "lista_posts"
```

### Modelo Perfil

Definido en `cuenta/models.py` y registrado en el admin (`cuenta/admin.py`):

```python
class Perfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil")
    biografia = models.TextField(blank=True)
    link_web = models.URLField(blank=True)
    avatar = models.ImageField(upload_to="avatares/", null=True, blank=True)
```

La relación `OneToOneField` garantiza que cada usuario tenga un único perfil.

### Señal: el perfil nace solo

En `cuenta/signals.py`, una señal `post_save` crea el perfil cada vez que se crea
un usuario, sin importar cómo (registro, admin o `createsuperuser`):

```python
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.get_or_create(user=instance)
```

La señal se registra en `cuenta/apps.py`, dentro de `ready()`:

```python
class CuentaConfig(AppConfig):
    name = "cuenta"

    def ready(self):
        from . import signals  # registra las señales
```

### Perfil público

`/cuenta/perfil/<usuario>/` muestra el nombre, `@usuario`, el avatar, la biografía,
el sitio web y la lista de **posts publicados** de ese usuario (los borradores no
aparecen). Si el usuario no existe, devuelve 404. Si es tu propio perfil, también
muestra los enlaces **Editar mi perfil** y **Cambiar contraseña**.

Se llega desde el nombre del autor en el detalle de cada post y en los comentarios,
y desde el "Hola, usuario" del menú.

### Usuarios sin perfil (casos límite)

Para que ningún usuario quede sin perfil:

| Caso | Cómo se cubre |
|------|---------------|
| Usuario nuevo (registro, admin o `createsuperuser`) | La señal `post_save` crea el perfil. En el registro va dentro de la misma transacción que el usuario. |
| Usuarios creados antes de existir el modelo `Perfil` | La migración `cuenta/migrations/0002_crear_perfiles_faltantes.py` les crea un perfil vacío al correr `migrate`. |
| Editar el perfil desde el admin | La ficha de cada usuario (`cuenta/admin.py`) muestra su perfil para editarlo. Al crear un usuario no aparece, porque la señal ya lo crea. |
| Red de seguridad | Las vistas de perfil usan `Perfil.objects.get_or_create(...)`: si algún usuario quedara sin perfil, se crea al entrar. |

### Avatares

- El avatar se guarda en `media/avatares/` (usa `MEDIA_URL` y `MEDIA_ROOT`, los mismos de las imágenes de los posts).
- `editar_perfil` procesa el archivo con `PerfilForm(request.POST, request.FILES, instance=perfil)`
  y el template usa `enctype="multipart/form-data"`.
- La página de perfil y el menú muestran el avatar solo si existe (`{% if perfil.avatar %}`).
- Desde **Editar perfil** también se pueden cambiar nombre, apellido y email.

### Rutas protegidas

Estas vistas usan `@login_required`. Si se entra sin sesión, redirigen a
`/cuenta/login/?next=...` y, después de iniciar sesión, vuelven a la página pedida:

| Ruta | Vista |
|------|-------|
| `/posts/nuevo/` | `crear_post` |
| `/posts/<slug>/editar/` | `editar_post` (además, solo el autor o un usuario con permiso `posts.change_post`) |
| `/posts/<slug>/eliminar/` | `eliminar_post` (además, solo el autor o un usuario con permiso `posts.change_post`) |
| `/mis-posts/` | `mis_posts` |
| `/cuenta/perfil/` | `perfil` |
| `/cuenta/perfil/editar/` | `editar_perfil` |
| `/cuenta/password/cambiar/` | `PasswordChangeView` (ya trae el login obligatorio) |

El listado (`/posts/`), el detalle (`/posts/<slug>/`) y el perfil público
(`/cuenta/perfil/<usuario>/`) son públicos.

### Contraseñas

Se usan las vistas que ya trae Django (`django.contrib.auth.views`), con templates
propios en `cuenta/templates/registration/`:

- **Cambiar contraseña** (logueado): desde el menú, **Mi perfil** o **Editar perfil**.
  Pide la contraseña actual y la nueva dos veces.
- **Recuperar contraseña:** desde el enlace **¿Olvidaste tu contraseña?** del login.
  Se ingresa el email, llega un mail con un enlace de un solo uso y ahí se elige
  la contraseña nueva.

En desarrollo el mail no se envía de verdad: aparece en la terminal donde corre
`runserver`, porque en `Config/settings.py` se usa el backend de consola:

```python
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}
```

### Navegación

El menú de `posts/base.html` cambia según `user.is_authenticated`:

- **Visitante anónimo:** Iniciar sesión, Registrarse.
- **Usuario logueado:** Crear post, Mis posts, Mi perfil (con su avatar), "Hola, usuario" (enlace a su perfil público), Cambiar contraseña y Cerrar sesión.

### Tests

```bash
python manage.py test
```

`cuenta/tests.py` prueba el registro (con creación del perfil), que la señal cree
el perfil (también para superusuarios y sin duplicarlo), los casos límite de usuarios
sin perfil, el perfil público (solo posts publicados y 404 si no existe), cambiar y
recuperar la contraseña por mail, el login y el logout, la redirección al login de
las rutas protegidas, la subida del avatar, **Mis posts** y el CRUD de posts.

`posts/test_proteccion.py` prueba las cuatro formas de proteger vistas (mixins, decoradores,
permiso propio y guardian), la página 403 y el comando `cargar_demo_auth`. En total son 54 tests.

## Publicar en PythonAnywhere

El sitio se puede publicar gratis en [PythonAnywhere](https://www.pythonanywhere.com/).
En todos los pasos, reemplazar `USUARIO` por tu nombre de usuario de PythonAnywhere.
La dirección del sitio queda `https://USUARIO.pythonanywhere.com`.

### Qué tiene el proyecto para producción

- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS` se leen del `.env`.
- `STATIC_ROOT = BASE_DIR / "staticfiles"`: ahí `collectstatic` junta los CSS (los del blog y los del admin).
- Con `DEBUG=False` se activan cookies seguras (solo HTTPS) y HSTS. `python manage.py check --deploy` no da avisos.
- Las imágenes subidas (`media/`) quedan guardadas en el disco de PythonAnywhere, que no se borra.

### 1. Descargar el proyecto y crear el entorno virtual

En PythonAnywhere, abrir **Consoles → Bash** y ejecutar:

```bash
git clone https://github.com/Belen2511/Proyecto-Final--Blog_Djando.git
cd Proyecto-Final--Blog_Djando
mkvirtualenv --python=/usr/bin/python3.13 blog-venv
pip install -r requirements.txt
```

Django 6.1 necesita Python 3.12 o más nuevo. Si `python3.13` no existe, cambiar la
imagen del sistema en **Account → System image** por la más nueva.

### 2. Crear el `.env` de producción

Generar una clave secreta nueva:

```bash
python -c "import secrets; print(secrets.token_urlsafe(60))"
```

Crear el archivo con `nano .env` (al lado de `manage.py`) y pegar, con la clave generada:

```
SECRET_KEY=la-clave-generada
DEBUG=False
ALLOWED_HOSTS=USUARIO.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://USUARIO.pythonanywhere.com
```

Guardar con `Ctrl + O`, `Enter` y salir con `Ctrl + X`.

### 3. Base de datos, estáticos y administrador

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py cargar_demo_auth
python manage.py check --deploy
```

`cargar_demo_auth` crea los usuarios de prueba (ver [Proteger vistas](#proteger-vistas)).
Como el sitio es público, conviene agregar al `.env` una contraseña propia para ellos
(`DEMO_PASSWORD=...`) antes de correrlo.

### 4. Crear la aplicación web

En la pestaña **Web**:

1. **Add a new web app** → **Manual configuration** (no elegir "Django") → **Python 3.13**.
2. **Code → Source code:** `/home/USUARIO/Proyecto-Final--Blog_Djando`
3. **Virtualenv:** `/home/USUARIO/.virtualenvs/blog-venv`
4. **Code → WSGI configuration file:** abrir el archivo, borrar todo y pegar:

```python
import os
import sys

path = "/home/USUARIO/Proyecto-Final--Blog_Djando"
if path not in sys.path:
    sys.path.insert(0, path)

os.environ["DJANGO_SETTINGS_MODULE"] = "Config.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

5. **Static files:** agregar dos filas.

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/USUARIO/Proyecto-Final--Blog_Djando/staticfiles` |
| `/media/` | `/home/USUARIO/Proyecto-Final--Blog_Djando/media` |

6. **Security → Force HTTPS:** activado.
7. Apretar el botón verde **Reload** y entrar a `https://USUARIO.pythonanywhere.com`.

### Actualizar el sitio después de subir cambios a GitHub

En la consola Bash de PythonAnywhere:

```bash
cd ~/Proyecto-Final--Blog_Djando
workon blog-venv
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Después, **Reload** en la pestaña **Web**.

### Si algo falla

- **Error log** (pestaña **Web**): muestra el error de Python si la página no carga.
- **Server log:** ahí aparecen los mails de "recuperar contraseña", porque en este proyecto
  los mails salen por consola y no se envían de verdad.
- **"Bad Request (400)":** revisar `ALLOWED_HOSTS` en el `.env`.
- **"CSRF verification failed" al enviar un formulario:** revisar `CSRF_TRUSTED_ORIGINS`.
- **El sitio se ve sin estilos:** revisar `collectstatic` y la fila `/static/` en **Static files**.
- En la cuenta gratis, el sitio se desactiva si no se entra a la pestaña **Web** y se aprieta
  **Run until 3 months from today** cada tanto.

## Proteger vistas

El blog muestra cuatro formas de proteger vistas: vistas con clases y mixins, decoradores,
un permiso propio en el modelo y permisos por objeto con **django-guardian**.

### Usuarios de prueba

```bash
python manage.py cargar_demo_auth
```

Crea los grupos **Editores** y **Publicadores**, cuatro usuarios y dos posts. La contraseña de
todos es `clave-demo-123`, o la que se ponga en `DEMO_PASSWORD` dentro del `.env`.
Se puede correr varias veces: no duplica nada.

| Usuario | Qué es | Qué puede |
|---------|--------|-----------|
| `ana`, `beto` | Autores comunes | Escribir y editar lo suyo. No pueden publicar (solo guardar borradores). |
| `carla` | Grupo **Editores** | Editar y eliminar posts ajenos, ver `/borradores/` y `/panel-editores/`. |
| `dani` | Grupo **Publicadores** | Tiene `posts.puede_publicar`: puede pasar un post a "Publicado". |

Un superusuario pasa **todas** las verificaciones de permisos, así que para probar permisos
conviene usar estos usuarios comunes.

### Dónde está cada forma de protección

| Forma | Archivo | Rutas para probar |
|-------|---------|-------------------|
| `LoginRequiredMixin` | `posts/views_cbv.py` → `PostCreateView` | `/cbv/nuevo/` |
| `UserPassesTestMixin` (solo quien puede modificar) | `posts/views_cbv.py` → `PostUpdateView`, `PostDeleteView` | `/posts/<slug>/cbv-editar/`, `/posts/<slug>/cbv-eliminar/` |
| `PermissionRequiredMixin` | `posts/views_cbv.py` → `BorradoresCbvView` | `/cbv/borradores/` |
| `@permission_required` | `posts/views.py` → `borradores` | `/borradores/` |
| `@user_passes_test` | `posts/views.py` → `panel_editores`, `es_editor` | `/panel-editores/` |
| Permiso propio (`Meta.permissions`) | `posts/models.py` (`puede_publicar`), `posts/forms.py` (`PostForm.clean_estado`) | publicar desde `/posts/nuevo/` |
| Permisos por objeto (guardian) | `posts/views.py` → `compartir_post`, `quitar_colaborador`, `mis_posts` | `/posts/<slug>/compartir/`, `/mis-posts/` |
| La regla que une todo | `posts/views.py` → `puede_modificar` | — |
| Configuración de guardian | `Config/settings.py` (`INSTALLED_APPS`, `AUTHENTICATION_BACKENDS`) | — |

### Cómo probarlo

1. **Redirección o 403.** `/borradores/` sin sesión → login. Como `ana` → página "Sin permiso" (403).
   Como `carla` → se ve la lista de borradores.
2. **`@user_passes_test`.** `/panel-editores/` como `ana` redirige al login aunque ya tenga sesión
   (así se comporta ese decorador). Como `carla`, abre.
3. **Permiso propio.** Como `ana`, crear un post con estado "Publicado" muestra
   "No tenés permiso para publicar". Como `dani`, se publica.
4. **Permiso por objeto.** Como `ana`, entrar a un post suyo → **Compartir** → `beto`. Como `beto`,
   **Mis posts** lo muestra en "Compartidos conmigo" y puede editarlo; los demás posts de `ana` siguen dando 403.
5. **Global frente a objeto.** `carla.has_perm("posts.change_post")` es `True`, pero
   `carla.has_perm("posts.change_post", post)` es `False`. Por eso `puede_modificar` pregunta por los dos.

### Cosas que conviene saber

- **Orden de los mixins.** Van antes de la vista genérica (`class X(LoginRequiredMixin, UpdateView)`).
  Al revés, no protegen y Django no avisa.
- **`raise_exception=True`** le da 403 también al visitante sin sesión. Por eso `borradores`
  apila `@login_required` arriba: visitante → login; con sesión y sin permiso → 403.
- **Dos backends y `login()`.** Con `ModelBackend` + guardian, `login(request, user)` necesita
  `backend="django.contrib.auth.backends.ModelBackend"` (ver `cuenta/views.py`).
- **Usuario `AnonymousUser`.** Guardian lo crea en la base al migrar. El formulario de compartir lo rechaza.
- **`accept_global_perms=False`** en `mis_posts`: sin eso, los Editores verían todos los posts
  como "compartidos conmigo".
