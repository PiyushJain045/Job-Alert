from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)       
def user_postsave(sender, instance, created, **kwargs):
    print("POSTSAVE")
    user = instance
    
    # add profile if user is created
    print("OK1")
    if created:
        print("OK2")
        Profile.objects.create(
            user = user,
        )
