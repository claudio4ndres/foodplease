"""Acá viven las clases del negocio"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .exceptions import PlatoInvalidoError


# esta clase representa un plato del menú con sus datos
@dataclass
class Plato:
    nombre: str
    descripcion: str
    precio: int
    disponible: bool = True
    id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None

    def __post_init__(self):
        self.validar()

    def validar(self):
        if not self.nombre or not self.nombre.strip():
            raise PlatoInvalidoError("El nombre del plato no puede estar vacío.")
        if self.precio <= 0:
            raise PlatoInvalidoError("El precio debe ser mayor que cero.")

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"
