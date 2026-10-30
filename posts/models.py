from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify


class ContenidoBase(models.Model):
    """Modelo abstracto con los campos comunes de Post y Comentario."""

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comentarios"
    )
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
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    contenido = models.TextField(blank=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default=BORRADOR,
    )
    imagen = models.ImageField(upload_to="posts/", null=True, blank=True)

    class Meta(ContenidoBase.Meta):
        # Permiso propio: se suma a add/change/delete/view.
        # Se consulta con user.has_perm("posts.puede_publicar").
        permissions = [("puede_publicar", "Puede publicar posts")]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        # Las vistas con clases (CreateView/UpdateView) redirigen acá al guardar.
        return reverse("detalle_post", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titulo)[:200] or "post"
            slug, n = base, 2
            while Post.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Comentario(ContenidoBase):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comentarios"
    )
    texto = models.TextField()

    class Meta(ContenidoBase.Meta):
        pass

    def __str__(self):
        return f"Comentario de {self.autor} en {self.post}"

