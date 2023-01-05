from django.contrib import admin
from django.contrib import admin
from .models import User



class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'firstname', 'lastname', 'email']


admin.site.register(User, UserAdmin)
