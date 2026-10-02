from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("acerca/", views.acerca, name="acerca"),
    path("posts/", views.lista_posts, name="lista_posts"),
    path("post/<int:pk>/", views.detalle_post, name="detalle_post"),
    path("nuevo/", views.nuevo_post, name="nuevo_post"),
]
