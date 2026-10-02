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
| `/posts/` | Listado de publicaciones |
| `/nuevo/` | Crear una publicación |

Para detener el servidor: `Ctrl + C`.

## Estructura

```
blog_django/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── blog_project/        # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py          # Incluye las rutas de posts con include()
│   ├── asgi.py
│   └── wsgi.py
└── posts/               # App principal del blog
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── urls.py          # Rutas de la app
    ├── views.py
    ├── migrations/
    ├── static/posts/css/
    │   └── estilos.css  # Estilos del sitio
    └── templates/posts/
        ├── base.html    # Layout base con menú de navegación
        ├── inicio.html
        ├── acerca.html
        ├── lista.html
        ├── detalle.html
        └── nuevo.html
```

## Templates y estilos

Todas las páginas extienden de `posts/base.html` con `{% extends 'posts/base.html' %}`
y rellenan el bloque `{% block content %}`. El CSS se carga desde
`posts/static/posts/css/estilos.css` con `{% static %}`.

## Aplicaciones

- `posts`: aplicación inicial para manejar las publicaciones del blog.
