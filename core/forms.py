from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from .models import PerfilUsuario, Actividad

# Validar el RUT de un usuario
def validar_rut(rut):
    # Eliminar puntos y guiones del RUT
    rut = rut.replace('.', '').replace('-', '')

    # Verificar que el RUT tenga el formato correcto
    if len(rut) < 2:
        return False

    # Separar el RUT y el dígito verificador
    rut_base = rut[:-1]
    dv = rut[-1].upper()

    # Calcular el dígito verificador
    suma = 0
    multiplicador = 2

    # Calcular la suma de los dígitos multiplicados por el multiplicador
    for digit in reversed(rut_base):
        suma += int(digit) * multiplicador
        multiplicador = multiplicador + 1 if multiplicador < 7 else 2

    dv_calculado = 11 - (suma % 11)
    
    # Determinar el dígito verificador calculado
    if dv_calculado == 11:
        dv_calculado = '0'
    elif dv_calculado == 10:
        dv_calculado = 'K'
    else:
        dv_calculado = str(dv_calculado)

    # Comparar el dígito verificador calculado con el ingresado
    return dv_calculado == dv

# Formulario para registrar un usuario
class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    RUT = forms.CharField(max_length=12)
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    # Validar el RUT del usuario
    def clean_RUT(self):
        rut = self.cleaned_data.get('RUT')
        if not validar_rut(rut):
            raise forms.ValidationError("El RUT ingresado no es válido.")
        return rut

    # Guardar el usuario y su perfil
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Django maneja la validación
        if commit:
            user.save()
            perfil = PerfilUsuario(user=user, RUT=self.cleaned_data['RUT'])
        perfil.save()
        return user

# Formulario para actualizar el perfil de un usuario
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

# Formulario de contacto
class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True, label='Nombre')
    email = forms.EmailField(required=True, label='Email')
    mensaje = forms.CharField(widget=forms.Textarea, required=True, label='Mensaje')