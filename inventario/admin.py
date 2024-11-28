from django.contrib import admin
from .models import Producto

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sku', 'cantidad', 'precio')
    search_fields = ('nombre', 'sku')

admin.site.register(Producto, ProductoAdmin)