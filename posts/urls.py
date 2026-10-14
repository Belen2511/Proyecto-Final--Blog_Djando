from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("acerca/", views.acerca, name="acerca"),
    path("posts/", views.lista_posts, name="lista_posts"),
    path("posts/nuevo/", views.crear_post, name="nuevo_post"),
    path("posts/<slug:slug>/", views.detalle_post, name="detalle_post"),
    path("posts/<slug:slug>/editar/", views.editar_post, name="editar_post"),
    path("posts/<slug:slug>/eliminar/", views.eliminar_post, name="eliminar_post"),
    path("estadisticas/", views.estadisticas, name="estadisticas"),
    path("contacto/", views.contacto, name="contacto"),
]
