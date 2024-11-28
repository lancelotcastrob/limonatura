from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    RUT = models.CharField(max_length=12, unique=True)
    perfil = models.CharField(max_length=10, choices=[
        ('admin', 'Administrador'),
        ('vendedor', 'Vendedor'),
        ('cliente', 'Cliente')
    ])

    def __str__(self):
        return f"{self.user.username} - {self.perfil}"

    def es_admin(self):
        return self.perfil == 'admin'
    
class Actividad(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.descripcion} - {self.fecha}"