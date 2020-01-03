#encoding:utf-8
from django.shortcuts import render
from django.conf import settings
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from videoJuegos.models import Genero, VideoJuego, Consola
from datetime import datetime
import re

# Create your views here.
path = "data"

def index(request):
    return render(request, 'index.html',{'STATIC_URL':settings.STATIC_URL})



def populateGeneros():
    print("Cargando Generos...")
    Genero.objects.all().delete()
    
    lista=[]
    fileobj=open(path+"\\datosGeneros.txt", "r")
    fileobj.seek(1)
    i=0
    for line in fileobj.readlines():
        if i!=0:
            lista.append(Genero(nombre=str(line.strip())))
        i=i+1
    fileobj.close()
    Genero.objects.bulk_create(lista)  # bulk_create hace la carga masiva para acelerar el proceso
    
    print("Género insertados: " + str(Genero.objects.count()))
    print("---------------------------------------------------------")
populateGeneros()


def populateVideoNintendoSwitch():
    print("Cargando videoJuegos nintendoSwitch...")
    VideoJuego.objects.filter(consola__nombre="Nintendo Switch").delete()
    dict_generos={}
    lista=[]
    listaAux=[]
    listaCompleta=[]
    lista
    fileobj=open(path+"\\datosNintendoSwitch.txt", "r")
    
 
    i=0
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')
        if len(rip) != 7:
            continue
        if  i!=0:
           
            u=VideoJuego(nombre=rip[0], precio=rip[1], consola=Consola.objects.get(nombre=rip[2]) ,urlProducto=rip[4], urlImg=rip[5], fechaLanzamiento=datetime.strptime(rip[6],'%d-%m-%Y'))
            lista.append(u)
        i=i+1   
    fileobj.close()
    VideoJuego.objects.bulk_create(lista)
    print("Cargando videoJuegos nintendoSwitch...")
    
    fileobj=open(path+"\\datosNintendoSwitch.txt", "r")
    i=0
    listaGeneros=[]
    dict_generos={}
    
    listaIdJuegos=[]
    for juegosNintendoSwitch in VideoJuego.objects.filter(consola__nombre="Nintendo Switch"):
                listaIdJuegos.append(juegosNintendoSwitch.idVideoJuegos)
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')
        if len(rip) != 7:
            continue
        if i!=0:
            listaString=str(rip[3])
            generos=(listaString.strip()).split(',')
            
            
            listaAux=[]
            for genero in generos:
                listaAux.append(Genero.objects.get(nombre=genero.strip("[ ' ]")))
            listaGeneros.append(listaAux)
    
        i=i+1
    print(listaGeneros)
    
    listaIdJuegos.sort(key=None, reverse=False)
    print(listaIdJuegos)
    dict_generos=dict(zip(listaIdJuegos,listaGeneros))
    print(dict_generos)
            
    
    dict2={}
   
    for juegosNintendoSwitch in VideoJuego.objects.filter(consola__nombre="Nintendo Switch"):
        juegosNintendoSwitch.generos.set(dict_generos[juegosNintendoSwitch.idVideoJuegos])
        dict2[juegosNintendoSwitch.idVideoJuegos]=juegosNintendoSwitch
    
    print("Videojuego insertados: " + str(VideoJuego.objects.count()))
    print("---------------------------------------------------------")

populateVideoNintendoSwitch()

