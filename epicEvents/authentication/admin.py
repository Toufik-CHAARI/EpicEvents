from django.contrib import admin
from authentication.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "pk", "role")


admin.site.register(CustomUser, CustomUserAdmin)
