from django.db import models


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField(blank=True)
    autor = models.CharField(max_length=100)
    likes = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        return self.titulo
