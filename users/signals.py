from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, CustomUser
from teams.models import Team

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs,):
    if created:
        Profile.objects.create(user=instance)