"""
Accounts app
============
Profile -> extends Django's built-in User with phone/address
           and tracks total completed orders for the loyalty program.
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    total_orders = models.PositiveIntegerField(
        default=0, help_text="Lifetime number of orders (drives loyalty rewards)")

    def __str__(self):
        return f"Profile of {self.user.username}"


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """Automatically create a Profile whenever a User is created."""
    if created:
        Profile.objects.create(user=instance)
    else:
        # Ensure profile exists for legacy users
        Profile.objects.get_or_create(user=instance)
