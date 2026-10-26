from django.contrib import admin
from .models import Store, Category, Order, OrderItem, Review

# Register your models here.
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'whose', 'price', 'date_create')
    list_filter = ('title', 'whose', 'date_create', 'price')
    search_fields = ('title',)
    ordering = ('-date_create',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 1
    fields = ['product', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'date', 'status']
    inlines = [OrderItemInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'created_at']
    search_fields = ('user',)