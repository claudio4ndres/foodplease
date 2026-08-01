from django import forms


# este formulario valida los datos que el usuario escribe al crear o editar un plato
class PlatoForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        label="Nombre",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    descripcion = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
    )
    precio = forms.IntegerField(
        label="Precio",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    disponible = forms.BooleanField(
        label="Disponible en Stock",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
