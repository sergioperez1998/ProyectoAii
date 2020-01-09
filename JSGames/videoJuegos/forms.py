from django import forms
from videoJuegos.models import Cliente

class ClienteForm(forms.ModelForm):
    
    class Meta:
        model= Cliente
        fields=[
            "nombre",
            "apellidos",
            "password",
            "edad",
            "sexo",
            "codigoPostal",
            "consolas",
            "videoJuegos",
            ]