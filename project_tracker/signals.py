from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Developer
from django.conf import settings    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_developer_for_new_user(sender, instance, created, **kwargs):
    print(instance)
    if created:
        Developer.objects.create(user=instance)   