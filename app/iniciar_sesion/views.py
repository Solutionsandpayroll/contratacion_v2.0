from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password

from .decorators import login_requerido
from .models import Usuario
from .forms import LoginForm


def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            contrasena = form.cleaned_data['contrasena']

            try:
                user = Usuario.objects.get(usuario=usuario)

                if check_password(contrasena, user.contrasena):

                    request.session['id_usuario'] = user.id_usuario
                    request.session['usuario'] = user.usuario

                    messages.success(request, 'Inicio de sesión exitoso')
                    return redirect('panel_admin')

                else:
                    messages.error(request, 'Contraseña incorrecta')

            except Usuario.DoesNotExist:
                messages.error(request, 'El usuario no existe')

    return render(request, 'login.html', {'form': form})


@login_requerido
def cerrar_sesion(request):
    request.session.flush()  # Elimina toda la sesión

    messages.success(
        request,
        'Has cerrado sesión correctamente.'
    )

    return redirect('login')