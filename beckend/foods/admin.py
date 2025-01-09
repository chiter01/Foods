from django.contrib import admin

from django.contrib import admin
from .models import Category, Food,Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['total_price']
    can_delete = True

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = "Итого"

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'total_price']
    search_fields = ['user__username']
    readonly_fields = ['total_price']
    inlines = [CartItemInline]

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = "Общая стоимость"

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'total_price']
    search_fields = ['product__name', 'cart__user__username']
    list_filter = ['cart__user']

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = "Итого"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_published','category', 'user', 'calories', 'weight')  
    list_filter = ('is_published', 'user','category', 'calories', 'weight')
    search_fields = ('name', 'description') 
    ordering = ('name',)
    list_editable = ('price', 'is_published')  
    list_per_page = 20  
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'is_published', 'image','category', 'user')
        }),
        ('Пищевая ценность', {
            'fields': ('proteins', 'fats', 'carbohydrates', 'calories', 'weight'),
            'classes': ('collapse',) 
        }),
    )
