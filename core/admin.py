from django.contrib import admin
from .models import PerfilUsuario
from django.urls import path
from .views import export_users_excel

class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'RUT', 'perfil', 'es_admin')  # Campos que se mostrarán en la lista
    search_fields = ('user__username', 'RUT')  # Campos por los que se puede buscar

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('exportar-usuarios/', self.admin_site.admin_view(self.export_users_excel), name='exportar_usuarios'),
        ]
        return custom_urls + urls

    def export_users_excel(self, request):
        return export_users_excel(request)

    def es_admin(self, obj):
        """Devuelve True si el perfil es 'admin'."""
        return obj.perfil == 'admin'
    es_admin.boolean = True  # Muestra un icono en lugar de True/False

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if response.status_code == 200:
            response.context_data['export_button'] = True
        return response

    def has_change_permission(self, request, obj=None):
        """Permitir cambios solo a administradores."""
        return request.user.perfilusuario.es_admin()

    def has_delete_permission(self, request, obj=None):
        """Permitir eliminación solo a administradores."""
        return request.user.perfilusuario.es_admin()

    def has_view_permission(self, request, obj=None):
        """Permitir ver solo a administradores y vendedores."""
        return request.user.perfilusuario.perfil in ['admin', 'vendedor']

# Registra el modelo en la administración
admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)