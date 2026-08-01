from typing import List, Optional

from menu.domain.entities import Plato
from menu.domain.ports import PlatoRepository
from menu.models import Plato as PlatoModel


class DjangoPlatoRepository(PlatoRepository):

    def listar(self) -> List[Plato]:
        return [self._a_entidad(m) for m in PlatoModel.objects.all().order_by('-fecha_creacion')]

    def obtener(self, plato_id: int) -> Optional[Plato]:
        try:
            return self._a_entidad(PlatoModel.objects.get(pk=plato_id))
        except PlatoModel.DoesNotExist:
            return None

    def guardar(self, plato: Plato) -> Plato:
        if plato.id is None:
            modelo = PlatoModel()
        else:
            modelo = PlatoModel.objects.get(pk=plato.id)
        modelo.nombre = plato.nombre
        modelo.descripcion = plato.descripcion
        modelo.precio = plato.precio
        modelo.disponible = plato.disponible
        modelo.save()
        return self._a_entidad(modelo)

    def eliminar(self, plato_id: int) -> None:
        PlatoModel.objects.filter(pk=plato_id).delete()

    # esta función convierte lo que viene de la base de datos en un objeto Plato
    @staticmethod
    def _a_entidad(modelo: PlatoModel) -> Plato:
        return Plato(
            id=modelo.pk,
            nombre=modelo.nombre,
            descripcion=modelo.descripcion,
            precio=modelo.precio,
            disponible=modelo.disponible,
            fecha_creacion=modelo.fecha_creacion,
        )
