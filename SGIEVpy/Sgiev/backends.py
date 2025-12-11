from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Usuarios


class UsuariosBackend(BaseBackend):
    def authenticate(self, request, correo=None, password=None, **kwargs):
        if correo is None or password is None:
            return None

        try:
            user = Usuarios.objects.get(correo=correo, activo=1)
        except Usuarios.DoesNotExist:
            return None

        # Comparar contra el hash guardado en "clave"
        if check_password(password, user.clave):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Usuarios.objects.get(pk=user_id, activo=1)
        except Usuarios.DoesNotExist:
            return None
