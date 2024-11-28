from .models import Producto

def agregar_stock(producto_id, cantidad_a_agregar):
    producto = Producto.objects.get(id=producto_id)
    producto.cantidad += cantidad_a_agregar
    producto.save()

def reducir_stock(producto_id, cantidad_a_reducir):
    producto = Producto.objects.get(id=producto_id)
    if producto.cantidad >= cantidad_a_reducir:
        producto.cantidad -= cantidad_a_reducir
        producto.save()
    else:
        raise ValueError("No hay suficiente stock disponible.")