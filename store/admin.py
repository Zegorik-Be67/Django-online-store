from django.contrib import admin
from .models import Store

# Register your models here.
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('title', 'whose', 'price', 'date_create')
    list_filter = ('title', 'whose', 'date_create', 'price')
    search_fields = ('title',)
    ordering = ('-date_create',)