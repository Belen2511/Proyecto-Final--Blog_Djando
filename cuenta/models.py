from django.conf import settings
from django.db import models


class Perfil(models.Model):
    """Información extra de cada usuario. Relación 1 a 1 con User."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil"
    )
    biografia = models.TextField(blank=True)
    link_web = models.URLField(blank=True)
    avatar = models.ImageField(upload_to="avatares/", null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
