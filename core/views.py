from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm, UserProfileForm
from .models import PerfilUsuario, Actividad
from openpyxl import Workbook
from django.http import HttpResponse

# Exportar usuarios a un archivo Excel
def export_users_excel(request):
    """Vista para exportar usuarios a un archivo Excel."""
    # Crear un libro de trabajo y una hoja
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Usuarios'

    # Encabezados de las columnas
    headers = ['Username', 'RUT', 'Perfil']
    sheet.append(headers)

    # Obtener todos los usuarios
    usuarios = PerfilUsuario.objects.select_related('user').all()
    
    # Agregar los datos de cada usuario
    for perfil in usuarios:
        sheet.append([perfil.user.username, perfil.RUT, perfil.perfil])

    # Configurar la respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=usuarios.xlsx'
    workbook.save(response)

    return response

# Registrar un usuario
def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()  # Esto llamará al método `save` que definiste
            return redirect('login')  # Redirige a la página de login después de registrar
    else:
        form = RegistroUsuarioForm()
    return render(request, 'core/registrar.html', {'form': form})

# Inicio de sesión de un usuario
def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'core/login.html')

# Cierre de sesión de un usuario
def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('index')

# Página de inicio
def index(request):
    return render(request, 'core/index.html')

# Página de perfil
def profile(request):
    user = request.user
    actividades_recientes = Actividad.objects.filter(usuario=user).order_by('-fecha')[:10]  # Obtener las 10 actividades más recientes

    context = {
        'user': user,
        'actividades_recientes': actividades_recientes,
    }

    return render(request, 'core/profile.html', context)

# Página de configuración
def settings(request):
    return render(request, 'core/settings.html')

# Página de ayuda
def help_view(request):
    return render(request, 'core/help.html')

# Actualizar perfil
@login_required
def actualizar_perfil(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # Crear una actividad al actualizar el perfil
            Actividad.objects.create(usuario=request.user, descripcion="Actualizó su perfil.")
            return redirect('perfil')  # Redirigir a la página de perfil
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'core/actualizar_perfil.html', {'form': form})