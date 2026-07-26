"""Acá se define qué se le puede pedir a un repositorio de platos.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from .entities import Plato


# esta clase define las funciones que debe tener cualquier repositorio de platos
class PlatoRepository(ABC):

    @abstractmethod
    def listar(self) -> List[Plato]:
        """Trae todos los platos, los más nuevos primero."""

    @abstractmethod
    def obtener(self, plato_id: int) -> Optional[Plato]:
        """Busca un plato por su id, devuelve None si no lo encuentra."""

    @abstractmethod
    def guardar(self, plato: Plato) -> Plato:
        """Guarda el plato: si es nuevo lo crea, si ya existe lo actualiza."""

    @abstractmethod
    def eliminar(self, plato_id: int) -> None:
        """Borra el plato con ese id."""
