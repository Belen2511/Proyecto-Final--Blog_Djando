# Blog Django

Proyecto base de un blog web desarrollado con Django.

## Descripción

Este repositorio contiene la estructura inicial de un proyecto Django para construir un blog.
Incluye la configuración base del proyecto (`blog_project`) y una aplicación llamada `posts`.

Configuración regional:

- Idioma: `es-ar`
- Zona horaria: `America/Argentina/Buenos_Aires`

## Requisitos

- Python 3.12 o superior
- Git

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Belen2511/blog_django.git
```

Entrar a la carpeta del proyecto:

```bash
cd blog_django
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
| `/posts/` | Listado de publicaciones publicadas |
| `/post/<id>/` | Detalle de una publicación |
| `/nuevo/` | Crear una publicación |
| `/admin/` | Panel de administración |

Para detener el servidor: `Ctrl + C`.

## Estructura

```
blog_django/
│
├── manage.py
├── README.md
├── requirements.txt
│
├── blog_project/
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

## Aplicaciones

- `posts`: aplicación inicial para manejar las publicaciones del blog.
