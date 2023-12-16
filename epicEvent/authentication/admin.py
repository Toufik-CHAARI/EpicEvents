from django.contrib import admin
from authentication.models import CustomUser




class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username","pk")
    
admin.site.register(CustomUser,CustomUserAdmin)