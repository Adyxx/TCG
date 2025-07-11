from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models.users import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("rank",)}),
    )

    list_display = ("username", "email", "rank", "is_staff", "is_superuser")
