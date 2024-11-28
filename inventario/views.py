from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .forms import ProductoForm
from .models import Producto
from .utils import agregar_stock, reducir_stock  # Importa las funciones

from django.shortcuts import render

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/lista_productos.html', {'productos': productos})

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')  # Redirige a donde desees
    else:
        form = ProductoForm()
    return render(request, 'inventario/agregar_producto.html', {'form': form})

def agregar_stock_view(request, producto_id):
    # Obtiene el producto o devuelve un 404 si no existe
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        # Obtiene la cantidad a agregar del formulario
        cantidad_a_agregar = int(request.POST.get('cantidad', 0))  # Proporciona un valor por defecto
        if cantidad_a_agregar > 0:  # Asegúrate de que la cantidad sea positiva
            producto.agregar_stock(cantidad_a_agregar)  # Llama al método del modelo
            messages.success(request, 'Stock agregado exitosamente.')
        else:
            messages.error(request, 'La cantidad a agregar debe ser mayor que cero.')
        
        return redirect('lista_productos')
    
    return render(request, 'inventario/agregar_stock.html', {'producto': producto})

def reducir_stock(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        cantidad_a_reducir = int(request.POST.get('cantidad', 0))
        
        if 0 < cantidad_a_reducir <= producto.cantidad:
            producto.cantidad -= cantidad_a_reducir
            producto.save()
            messages.success(request, f'Se ha reducido el stock de {producto.nombre} en {cantidad_a_reducir}.')
            return redirect('lista_productos')  # Redirigir a la página deseada
        else:
            messages.error(request, 'Cantidad no válida para reducir.')

    return render(request, 'inventario/reducir_stock.html', {'producto': producto})