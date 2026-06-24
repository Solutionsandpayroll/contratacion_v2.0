from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=255)

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return self.usuario