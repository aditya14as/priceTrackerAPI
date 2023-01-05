from django.contrib import admin
from .models import Bitcoin

# Register your models here.


class Price(admin.ModelAdmin):
    list_display = ['id', 'price', 'time']


admin.site.register(Bitcoin, Price)
