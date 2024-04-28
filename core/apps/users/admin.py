from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'role',
        'first_name',
        'last_name',
        'phone',
        'telegram',
        'is_active',
        'is_staff'
    )
