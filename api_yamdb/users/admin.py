from django.contrib import admin
from django.contrib.auth.admin import CustomUserAdmin

from .models import CustomUser

CustomUserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('bio', 'role',)}),
)
admin.site.register(CustomUser, CustomUserAdmin)
