from django.db import models


# este modelo crea la tabla de platos en la base de datos
class Plato(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.IntegerField()
    disponible = models.BooleanField(default=True, verbose_name="Disponible en Stock")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"