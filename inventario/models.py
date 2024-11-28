from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    sku = models.CharField(max_length=50, unique=True)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    
    def agregar_stock(self, cantidad_a_agregar):
        self.cantidad += cantidad_a_agregar
        self.save()

    def reducir_stock(self, cantidad_a_reducir):
        if self.cantidad >= cantidad_a_reducir:
            self.cantidad -= cantidad_a_reducir
            self.save()
        else:
            raise ValueError("No hay suficiente stock disponible.")

    def __str__(self):
        return self.nombre