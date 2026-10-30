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
│   ├── migrations/
│   │
│   ├── templates/
│   │   └── posts/
│   │       ├── base.html
│   │       ├── inicio.html
│   │       ├── acerca.html
│   │       ├── lista_posts.html
│   │       ├── detalle_post.html
│   │       ├── mis_posts.html
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

`requirements.txt` incluye **Django**, **Pillow** (para `ImageField`) y
**python-decouple** (para leer el `.env`). Se actualiza con:

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
