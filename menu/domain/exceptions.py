"""Errores propios del negocio."""

class PlatoInvalidoError(Exception):
    """Se lanza cuando el plato tiene datos incorrectos (sin nombre, precio en cero, etc.)."""


class PlatoNoEncontradoError(Exception):
    """Se lanza cuando se busca un plato que no existe."""
