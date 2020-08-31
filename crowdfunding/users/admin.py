from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomerUserAdmin(UserAdmin):
    pass

admin.site.register (get_user_model(), CustomUserAdmin)