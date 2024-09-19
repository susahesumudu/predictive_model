from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Lab Assistant', 'Lab Assistant'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    nic_passport_no = models.CharField(max_length=30, verbose_name="NIC/Passport No.")
    contact_address = models.TextField(verbose_name="Contact Address")
    permanent_address = models.TextField(verbose_name="Permanent Address", blank=True, null=True)
    mobile_no = models.CharField(max_length=15, verbose_name="Mobile No.")
    home_no = models.CharField(max_length=15, blank=True, null=True, verbose_name="Home Telephone")
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male')
    email = models.EmailField(verbose_name="Email")
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"



# Automatically create a profile for each new user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Automatically save the profile when the user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

