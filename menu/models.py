from django.db import models

# Create your models here.
from django.db import models

class Plato(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.IntegerField()
    disponible = models.BooleanField(default=True, verbose_name="Disponible en Stock")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"