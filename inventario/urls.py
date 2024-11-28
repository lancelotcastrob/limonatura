from django.urls import path
from .views import agregar_producto, agregar_stock_view, reducir_stock, lista_productos

urlpatterns = [
    path('agregar/', agregar_producto, name='agregar_producto'),
    path('productos/agregar-stock/<int:producto_id>/', agregar_stock_view, name='agregar_stock'),
    path('reducir_stock/<int:producto_id>/', reducir_stock, name='reducir_stock'),
    path('productos/', lista_productos, name='lista_productos'),
    # Otras URLs que necesites
]