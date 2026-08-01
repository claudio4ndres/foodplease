from django.http import Http404
from django.shortcuts import redirect, render

from menu.application.use_cases import (
    CrearPlato,
    EditarPlato,
    EliminarPlato,
    ListarPlatos,
    ObtenerPlato,
)
from menu.domain.exceptions import PlatoInvalidoError, PlatoNoEncontradoError
from menu.infrastructure.repositories import DjangoPlatoRepository
from menu.presentation.forms import PlatoForm

# este es el repositorio que usan todas las vistas para guardar y leer platos
repositorio = DjangoPlatoRepository()


# READ: Listar Platos
def lista_platos(request):
    platos = ListarPlatos(repositorio).ejecutar()
    return render(request, 'menu/pages/lista_platos.html', {'platos': platos})


# CREATE: Agregar Plato
def crear_plato(request):
    if request.method == 'POST':
        form = PlatoForm(request.POST)
        if form.is_valid():
            try:
                CrearPlato(repositorio).ejecutar(**form.cleaned_data)
                return redirect('lista_platos')
            except PlatoInvalidoError as error:
                form.add_error(None, str(error))
    else:
        form = PlatoForm()
    return render(request, 'menu/pages/form_plato.html', {'form': form, 'titulo': 'Agregar Nuevo Plato'})


# UPDATE: Editar Plato
def editar_plato(request, pk):
    plato = _obtener_o_404(pk)
    if request.method == 'POST':
        form = PlatoForm(request.POST)
        if form.is_valid():
            try:
                EditarPlato(repositorio).ejecutar(plato_id=pk, **form.cleaned_data)
                return redirect('lista_platos')
            except PlatoInvalidoError as error:
                form.add_error(None, str(error))
    else:
        form = PlatoForm(initial={
            'nombre': plato.nombre,
            'descripcion': plato.descripcion,
            'precio': plato.precio,
            'disponible': plato.disponible,
        })
    return render(request, 'menu/pages/form_plato.html', {'form': form, 'titulo': 'Editar Plato'})


# DELETE: Eliminar Plato
def eliminar_plato(request, pk):
    plato = _obtener_o_404(pk)
    if request.method == 'POST':
        EliminarPlato(repositorio).ejecutar(pk)
        return redirect('lista_platos')
    return render(request, 'menu/pages/confirmar_eliminar.html', {'plato': plato})


def _obtener_o_404(pk):
    try:
        return ObtenerPlato(repositorio).ejecutar(pk)
    except PlatoNoEncontradoError:
        raise Http404
