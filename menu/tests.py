from django.test import TestCase
from django.urls import reverse

from menu.application.use_cases import CrearPlato, EditarPlato, EliminarPlato, ListarPlatos
from menu.domain.entities import Plato
from menu.domain.exceptions import PlatoInvalidoError, PlatoNoEncontradoError
from menu.domain.ports import PlatoRepository
from menu.models import Plato as PlatoModel


# este repositorio guarda los platos en un diccionario, lo usamos para las pruebas
class RepositorioEnMemoria(PlatoRepository):
    
    def __init__(self):
        self._platos = {}
        self._siguiente_id = 1

    def listar(self):
        return sorted(self._platos.values(), key=lambda p: p.id, reverse=True)

    def obtener(self, plato_id):
        return self._platos.get(plato_id)

    def guardar(self, plato):
        if plato.id is None:
            plato.id = self._siguiente_id
            self._siguiente_id += 1
        self._platos[plato.id] = plato
        return plato

    def eliminar(self, plato_id):
        self._platos.pop(plato_id, None)


class CasosDeUsoTest(TestCase):
    """Prueba la lógica de negocio de forma aislada, sin Django ORM ni HTTP."""

    def setUp(self):
        self.repo = RepositorioEnMemoria()

    def test_crear_y_listar_plato(self):
        CrearPlato(self.repo).ejecutar('Completo', 'Con palta y tomate', 3500, True)
        platos = ListarPlatos(self.repo).ejecutar()
        self.assertEqual(len(platos), 1)
        self.assertEqual(platos[0].nombre, 'Completo')

    def test_precio_invalido_es_rechazado_por_el_dominio(self):
        with self.assertRaises(PlatoInvalidoError):
            CrearPlato(self.repo).ejecutar('Completo', 'Con palta', 0, True)

    def test_nombre_vacio_es_rechazado_por_el_dominio(self):
        with self.assertRaises(PlatoInvalidoError):
            Plato(nombre='   ', descripcion='x', precio=1000)

    def test_editar_plato(self):
        plato = CrearPlato(self.repo).ejecutar('Completo', 'Con palta', 3500, True)
        EditarPlato(self.repo).ejecutar(plato.id, 'Completo Italiano', 'Palta, tomate, mayo', 3900, False)
        editado = self.repo.obtener(plato.id)
        self.assertEqual(editado.nombre, 'Completo Italiano')
        self.assertFalse(editado.disponible)

    def test_eliminar_plato_inexistente_lanza_error(self):
        with self.assertRaises(PlatoNoEncontradoError):
            EliminarPlato(self.repo).ejecutar(999)


class VistasCrudTest(TestCase):
    """Prueba el flujo completo: HTTP -> vista -> caso de uso -> ORM -> SQLite."""

    def test_lista_vacia(self):
        respuesta = self.client.get(reverse('lista_platos'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'No hay platos registrados')

    def test_crear_plato(self):
        respuesta = self.client.post(reverse('crear_plato'), {
            'nombre': 'Chorrillana',
            'descripcion': 'Papas, carne, huevo',
            'precio': 12000,
            'disponible': 'on',
        })
        self.assertRedirects(respuesta, reverse('lista_platos'))
        self.assertEqual(PlatoModel.objects.count(), 1)

    def test_crear_plato_con_precio_cero_muestra_error(self):
        respuesta = self.client.post(reverse('crear_plato'), {
            'nombre': 'Chorrillana',
            'descripcion': 'Papas, carne, huevo',
            'precio': 0,
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'El precio debe ser mayor que cero.')
        self.assertEqual(PlatoModel.objects.count(), 0)

    def test_editar_plato(self):
        modelo = PlatoModel.objects.create(nombre='Sopaipilla', descripcion='Con pebre', precio=500)
        respuesta = self.client.post(reverse('editar_plato', args=[modelo.pk]), {
            'nombre': 'Sopaipilla pasada',
            'descripcion': 'Con chancaca',
            'precio': 800,
            'disponible': 'on',
        })
        self.assertRedirects(respuesta, reverse('lista_platos'))
        modelo.refresh_from_db()
        self.assertEqual(modelo.nombre, 'Sopaipilla pasada')

    def test_eliminar_plato(self):
        modelo = PlatoModel.objects.create(nombre='Barros Luco', descripcion='Carne y queso', precio=6500)
        respuesta = self.client.post(reverse('eliminar_plato', args=[modelo.pk]))
        self.assertRedirects(respuesta, reverse('lista_platos'))
        self.assertEqual(PlatoModel.objects.count(), 0)

    def test_editar_plato_inexistente_devuelve_404(self):
        respuesta = self.client.get(reverse('editar_plato', args=[999]))
        self.assertEqual(respuesta.status_code, 404)
