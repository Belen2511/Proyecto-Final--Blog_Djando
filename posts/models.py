from django.db import models


class ContenidoBase(models.Model):
    """Modelo abstracto con los campos comunes de Post y Comentario."""

    autor = models.CharField(max_length=100)
    likes = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-fecha_creacion"]


class Post(ContenidoBase):
    BORRADOR = "borrador"
    PUBLICADO = "publicado"
    ARCHIVADO = "archivado"
    ESTADOS = [
        (BORRADOR, "Borrador"),
        (PUBLICADO, "Publicado"),
        (ARCHIVADO, "Archivado"),
    ]

    titulo = models.CharField(max_length=200)
    contenido = models.TextField(blank=True)
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default=BORRADOR,
    )

    class Meta(ContenidoBase.Meta):
        pass

    def __str__(self):
        return self.titulo


class Comentario(ContenidoBase):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comentarios"
    )
    texto = models.TextField()

    class Meta(ContenidoBase.Meta):
        pass

    def __str__(self):
        return f"Comentario de {self.autor} en {self.post}"

