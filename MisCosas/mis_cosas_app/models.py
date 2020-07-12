from django.db import models

# Create your models here.
class Alimentador(models.Model):
    id_canal = models.CharField(max_length=64)
    nombre = models.CharField(max_length=64)
    enlace = models.URLField()
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
