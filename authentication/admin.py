from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authentication.models import User
# Register your models here.

# class AdminUser(UserAdmin):
    
admin.site.register(User,UserAdmin)
