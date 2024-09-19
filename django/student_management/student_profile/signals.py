from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import StudentProfile

# Signal to create StudentProfile when a User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)

# Signal to save StudentProfile when a User is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.studentprofile.save()

