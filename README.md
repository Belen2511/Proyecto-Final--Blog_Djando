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

Para detener el servidor: `Ctrl + C`.

## Estructura

```
blog_django/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── blog_project/        # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── posts/               # App principal del blog
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations/
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py
```

## Aplicaciones

- `posts`: aplicación inicial para manejar las publicaciones del blog.
