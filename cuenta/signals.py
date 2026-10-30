from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Perfil


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_perfil(sender, instance, created, **kwargs):
    """Cada vez que se crea un User (registro, admin, createsuperuser) nace su Perfil."""
    if created:
        Perfil.objects.get_or_create(user=instance)
