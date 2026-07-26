from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Plato
from .forms import PlatoForm

# READ: Listar Platos
def lista_platos(request):
    platos = Plato.objects.all().order_by('-fecha_creacion')
    return render(request, 'menu/lista_platos.html', {'platos': platos})

# CREATE: Agregar Plato
def crear_plato(request):
    if request.method == 'POST':
        form = PlatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_platos')
    else:
        form = PlatoForm()
    return render(request, 'menu/form_plato.html', {'form': form, 'titulo': 'Agregar Nuevo Plato'})

# UPDATE: Editar Plato
def editar_plato(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == 'POST':
        form = PlatoForm(request.POST, instance=plato)
        if form.is_valid():
            form.save()
            return redirect('lista_platos')
    else:
        form = PlatoForm(instance=plato)
    return render(request, 'menu/form_plato.html', {'form': form, 'titulo': 'Editar Plato'})

# DELETE: Eliminar Plato
def eliminar_plato(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == 'POST':
        plato.delete()
        return redirect('lista_platos')
    return render(request, 'menu/confirmar_eliminar.html', {'plato': plato})