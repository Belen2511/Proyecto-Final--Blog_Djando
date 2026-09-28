from django.urls import path

from . import views

urlpatterns = [
    path("", views.lista_posts, name="lista_posts"),
    path("post/<int:pk>/", views.detalle_post, name="detalle_post"),
    path("nuevo/", views.nuevo_post, name="nuevo_post"),
]
