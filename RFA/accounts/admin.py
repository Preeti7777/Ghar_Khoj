from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": ("role", "phone", "profile_image", "citizenship_front_image", "citizenship_back_image", "photo_with_citizenship")
        }),
    )

admin.site.register(User, CustomUserAdmin)