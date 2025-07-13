from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):  
    list_display = ['id', 'username', 'email', 'phone', 'is_theatre_manager', 'is_approved', 'otp_verified']


# Register your models here.
