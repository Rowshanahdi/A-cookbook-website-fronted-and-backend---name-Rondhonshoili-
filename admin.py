from django.contrib import admin
from .models import Product, CartItem
from .models import Recipe, SavedRecipe

admin.site.register(Recipe)
admin.site.register(SavedRecipe)

from django.contrib import admin
from .models import Order, OrderItem

from django.contrib import admin
from .models import Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total', 'created_at']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
















from django.contrib import admin
from .models import Product, CartItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']
















from django.contrib import admin
from .models import FreeClassRegistration, PaidClassRegistration

@admin.register(FreeClassRegistration)
class FreeClassAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'contact_number', 'email', 'user', 'date_registered')
    search_fields = ('full_name', 'email', 'contact_number')

@admin.register(PaidClassRegistration)
class PaidClassAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'contact_number', 'email', 'transaction_id', 'user', 'date_registered')
    search_fields = ('full_name', 'transaction_id', 'email')





















from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'country', 'enquiry_for', 'subject', 'created_at', 'user')
    list_filter = ('created_at', 'country', 'enquiry_for')
    search_fields = ('full_name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)




























from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('recipe__title', 'user__username', 'comment')
    date_hierarchy = 'created_at'










