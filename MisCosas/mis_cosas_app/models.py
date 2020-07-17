from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Alimentador(models.Model):
    id_canal = models.CharField(max_length=64)
    nombre = models.CharField(max_length=64)
    enlace = models.URLField()
    seleccionado = models.BooleanField(default=True)
    votos = models.IntegerField(default = 0)
    tipo = models.CharField(max_length=64, null = True)
    def __str__(self):
        return self.nombre


class Item(models.Model):
    alimentador = models.ForeignKey(Alimentador, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=64)
    id = models.CharField(max_length=64, primary_key=True)
    enlace = models.URLField()
    descripcion = models.CharField(max_length=1024, null=True) # Para YouTube
    foto = models.URLField(null = True) # Para Flickr
    votos = models.IntegerField(default = 0)

    def __str__(self):
        return self.nombre


class FotoDePerfil(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to = "media", default="PERFIL-HUEVO.jpg")

    def __str__(self):
        return self.usuario.username

class Usuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tema_oscuro = models.BooleanField(default=False)
    def __str__(self):
        return self.usuario.username

class Voto(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    voto_positivo = models.BooleanField(default=False)
    voto_negativo = models.BooleanField(default=False)
    fecha = models.DateTimeField(null=True)

    def __str__(self):
        return self.item.nombre

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=256)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    fecha = models.DateTimeField()

    def __str__(self):
        return "Comentario de " + self.usuario.username + " en el ítem " + self.item.nombre
