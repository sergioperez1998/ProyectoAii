from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from videoJuegos.models import Cliente, Consola
from django import forms

class CustomUserForm(UserCreationForm):
    
    class Meta:
        model=User
        fields=["first_name", "last_name", "email", "username", "password1", "password2"]
        
class ClienteForm(forms.Form):
    '''
    consolas = Consola.objects.all()
    OPTIONS = []
    for c in consolas:
        OPTIONS.append(c.nombre)
    '''
    OPTIONS = ["A","B","C"]
    
    Consolas = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=OPTIONS)
    
class BusquedaPorGeneroForm(forms.Form):
    genero = forms.CharField(label="genero", widget=forms.TextInput, required=True)