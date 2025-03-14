from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "reg_number", "is_admin", "is_superuser"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("reg_number", "is_admin")}),)

admin.site.register(CustomUser, CustomUserAdmin)
