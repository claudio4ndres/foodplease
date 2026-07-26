from django.urls import path
from menu.presentation import views

urlpatterns = [
    path('', views.lista_platos, name='lista_platos'),
    path('crear/', views.crear_plato, name='crear_plato'),
    path('editar/<int:pk>/', views.editar_plato, name='editar_plato'),
    path('eliminar/<int:pk>/', views.eliminar_plato, name='eliminar_plato'),
]
