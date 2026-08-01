from typing import List

from menu.domain.entities import Plato
from menu.domain.exceptions import PlatoNoEncontradoError
from menu.domain.ports import PlatoRepository


# esta clase se encarga de traer todos los platos del menú
class ListarPlatos:
    def __init__(self, repositorio: PlatoRepository):
        self.repositorio = repositorio

    def ejecutar(self) -> List[Plato]:
        return self.repositorio.listar()


class ObtenerPlato:
    def __init__(self, repositorio: PlatoRepository):
        self.repositorio = repositorio

    def ejecutar(self, plato_id: int) -> Plato:
        plato = self.repositorio.obtener(plato_id)
        if plato is None:
            raise PlatoNoEncontradoError(f"No existe un plato con id {plato_id}.")
        return plato


class CrearPlato:
    def __init__(self, repositorio: PlatoRepository):
        self.repositorio = repositorio

    def ejecutar(self, nombre: str, descripcion: str, precio: int, disponible: bool) -> Plato:
        plato = Plato(nombre=nombre, descripcion=descripcion, precio=precio, disponible=disponible)
        return self.repositorio.guardar(plato)


class EditarPlato:
    def __init__(self, repositorio: PlatoRepository):
        self.repositorio = repositorio

    def ejecutar(self, plato_id: int, nombre: str, descripcion: str, precio: int, disponible: bool) -> Plato:
        plato = ObtenerPlato(self.repositorio).ejecutar(plato_id)
        plato.nombre = nombre
        plato.descripcion = descripcion
        plato.precio = precio
        plato.disponible = disponible
        plato.validar()
        return self.repositorio.guardar(plato)


class EliminarPlato:
    def __init__(self, repositorio: PlatoRepository):
        self.repositorio = repositorio

    def ejecutar(self, plato_id: int) -> None:
        ObtenerPlato(self.repositorio).ejecutar(plato_id)
        self.repositorio.eliminar(plato_id)
