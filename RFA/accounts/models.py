from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField


class User(AbstractUser):

    class Role(models.TextChoices):
        TENANT = "TENANT", "Tenant"
        LANDLORD = "LANDLORD", "Landlord"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.TENANT
    )

    phone = models.CharField(max_length=15, blank=True, null=True)

    profile_image = CloudinaryField(
        'image',
        blank=True,
        null=True
    )
    citizenship_front_image = CloudinaryField(
        'citizenship_front',
        blank=True,
        null=True
    )

    citizenship_back_image = CloudinaryField(
        'citizenship_back',
        blank=True,
        null=True
    )
    photo_with_citizenship = CloudinaryField(
        'photo_with_citizenship',
        blank=True,
        null=True
    )

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.username
    
    def __str__(self):
        return f"{self.username} ({self.role})"