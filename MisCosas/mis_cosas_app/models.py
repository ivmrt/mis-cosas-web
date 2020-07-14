from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Alimentador(models.Model):
    id_canal = models.CharField(max_length=64)
    nombre = models.CharField(max_length=64)
    enlace = models.URLField()
    seleccionado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre


class Item(models.Model):
    alimentador = models.ForeignKey(Alimentador, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=64)
    id = models.CharField(max_length=64, primary_key=True)
    enlace = models.URLField()
    descripcion = models.CharField(max_length=1024, null=True)
    def __str__(self):
        return self.nombre


class FotoDePerfil(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to = "media", default="PERFIL-HUEVO.jpg")
