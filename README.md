# Blog Django

Proyecto base de un blog web desarrollado con Django.

## Descripción

Este repositorio contiene la estructura inicial de un proyecto Django para construir un blog.
Incluye la configuración base del proyecto (`Config`) y una aplicación llamada `posts`.

Configuración regional:

- Idioma: `es-ar`
- Zona horaria: `America/Argentina/Buenos_Aires`

## Requisitos

- Python 3.12 o superior
- Git

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Belen2511/Proyecto-Blog_Django.git
```

Entrar a la carpeta del proyecto:

```bash
cd Proyecto-Blog_Django
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

Crear la base de datos (aplica las migraciones del modelo `Post`):

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

## Capturas

Página de inicio (`/`):

![Página de inicio del blog](capturas/pagina_inicio.png)

Panel de administración de Django (`/admin/`), con el modelo `Post` registrado:

![Panel de administración de Django](capturas/admin_django.png)

## Estructura

```
blog_django/
│
├── manage.py
├── README.md
├── requirements.txt
│
├── Config/
│   ├── settings.py
│   └── urls.py
│
└── posts/
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── urls.py
    ├── views.py
    │
    ├── templates/
    │   └── posts/
    │       ├── base.html
    │       ├── inicio.html
    │       ├── lista_posts.html
    │       ├── detalle.html
    │       ├── nuevo.html
    │       └── acerca.html
    │
    └── static/
        └── posts/
            └── css/
                └── estilos.css
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

La view `lista_posts` (en `posts/views.py`) trae desde la base de datos solo los
posts publicados, del más reciente al más antiguo, y los envía al template
mediante el contexto:

```python
def lista_posts(request):
    posts = Post.objects.filter(estado="publicado").order_by("-fecha_creacion")
    promedio = posts.aggregate(promedio=Avg("likes"))["promedio"] or 0
    mas_popular = posts.order_by("-likes").first()
    context = {
        "posts": posts,
        "promedio": round(promedio, 1),
        "mas_popular": mas_popular,
    }
    return render(request, "posts/lista_posts.html", context)
```

Los posts en estado borrador o archivado no aparecen en `/posts/`.

## Templates y estilos

Todas las páginas extienden de `posts/base.html` con `{% extends 'posts/base.html' %}`
y rellenan el bloque `{% block content %}`. El CSS se carga desde
`posts/static/posts/css/estilos.css` con `{% static %}`.

En `posts/templates/posts/lista_posts.html` se recorren las publicaciones con un
bucle `{% for post in posts %}` y se muestra de cada una el título, el contenido,
el autor, el estado, la fecha de creación y los likes:

```html
{% for post in posts %}
<a class="card" href="{% url 'detalle_post' post.pk %}">
    <h2>{{ post.titulo }}</h2>
    <p>{{ post.contenido|linebreaksbr }}</p>
    <div class="meta">
        por {{ post.autor }} — {{ post.get_estado_display }} — {{ post.fecha_creacion|date:"d/m/Y H:i" }} — {{ post.likes }} likes
    </div>
</a>
{% empty %}
<p class="stats">Todavía no hay posts.</p>
{% endfor %}
```

## Checkpoint: Modelos y Admin configurados

Commit de este checkpoint: `Checkpoint: Modelos y Admin configurados.`

En este punto del proyecto quedó listo:

- El modelo `Post` (`titulo`, `contenido`, `autor`, `likes`, `fecha_creacion`, `estado`) definido en `posts/models.py`, con sus migraciones aplicadas.
- El modelo `Post` registrado en el panel de administración (`posts/admin.py`), desde donde se pueden crear, editar y borrar publicaciones (ver la captura del admin en la sección [Capturas](#capturas)).

## Aplicaciones

- `posts`: aplicación inicial para manejar las publicaciones del blog.

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
`contenido`, `autor`, `estado` e `imagen`.

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

Después de actualizar el modelo hay que aplicar la migración (`0005_post_imagen`):

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
