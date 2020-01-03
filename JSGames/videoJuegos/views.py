#encoding:utf-8
from django.shortcuts import render
from django.conf import settings
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from videoJuegos.models import Genero, VideoJuego, Consola
from datetime import datetime


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



def populateVideoJuegosNintendoSwitch():
    print("Cargando videoJuegos nintendoSwitch...")
    VideoJuego.objects.filter(consola__nombre="Nintendo Switch").delete()
    lista=[]
    listaAux=[]
    listaGeneros=[]
    dict_generos={}
    listaIdJuegos=[]
    fileobj=open(path+"\\datosNintendoSwitch.txt", "r")
    
 
    i=0
    
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')
        if len(rip) != 7:
            continue
        if  i!=0:
             
                 
            listaString=str(rip[3])
            generos=(listaString.strip()).split(',')
            
            
            listaAux=[]
            for genero in generos:
                listaAux.append(Genero.objects.get(nombre=genero.strip("[ ' ]")))
            listaGeneros.append(listaAux)
           
            u=VideoJuego(nombre=rip[0], precio=rip[1], consola=Consola.objects.get(nombre=rip[2]) ,urlProducto=rip[4], urlImg=rip[5], fechaLanzamiento=datetime.strptime(rip[6],'%d-%m-%Y'))
            lista.append(u)
        i=i+1   
    fileobj.close()
    VideoJuego.objects.bulk_create(lista)
    
    for juegosNintendoSwitch in VideoJuego.objects.filter(consola__nombre="Nintendo Switch"):
                listaIdJuegos.append(juegosNintendoSwitch.idVideoJuegos)
    
    listaIdJuegos.sort(key=None, reverse=False)
    dict_generos=dict(zip(listaIdJuegos,listaGeneros))
    
    dict2={}
   
    for juegosNintendoSwitch in VideoJuego.objects.filter(consola__nombre="Nintendo Switch"):
        juegosNintendoSwitch.generos.set(dict_generos[juegosNintendoSwitch.idVideoJuegos])
        dict2[juegosNintendoSwitch.idVideoJuegos]=juegosNintendoSwitch
    
    print("Videojuego insertados: " + str(VideoJuego.objects.filter(consola__nombre="Nintendo Switch").count()))
    print("---------------------------------------------------------")


populateVideoJuegosNintendoSwitch()


def populateVideoJuegosPc():
    print("Cargando videoJuegos de Pc...")
    VideoJuego.objects.filter(consola__nombre="Pc").delete()
    lista=[]
    listaAux=[]
    listaGeneros=[]
    dict_generos={}
    listaIdJuegos=[]
    fileobj=open(path+"\\datosPc.txt", "r")
    
 
    i=0
    
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')
        if len(rip) != 7:
            continue
        if  i!=0:
             
                 
            listaString=str(rip[3])
            generos=(listaString.strip()).split(',')
            
            
            listaAux=[]
            for genero in generos:
                listaAux.append(Genero.objects.get(nombre=genero.strip("[ ' ]")))
            listaGeneros.append(listaAux)
           
            u=VideoJuego(nombre=rip[0], precio=rip[1], consola=Consola.objects.get(nombre=rip[2]) ,urlProducto=rip[4], urlImg=rip[5], fechaLanzamiento=datetime.strptime(rip[6],'%d-%m-%Y'))
            lista.append(u)
        i=i+1   
    fileobj.close()
    VideoJuego.objects.bulk_create(lista)
    
    for juegosPc in VideoJuego.objects.filter(consola__nombre="Pc"):
                listaIdJuegos.append(juegosPc.idVideoJuegos)
    
    listaIdJuegos.sort(key=None, reverse=False)
    dict_generos=dict(zip(listaIdJuegos,listaGeneros))
    
    
    
    listaIdJuegos.sort(key=None, reverse=False)
    dict_generos=dict(zip(listaIdJuegos,listaGeneros))
    
    dict2={}
   
    for juegosPc in VideoJuego.objects.filter(consola__nombre="Pc"):
        juegosPc.generos.set(dict_generos[juegosPc.idVideoJuegos])
        dict2[juegosPc.idVideoJuegos]=juegosPc
    
    print("Videojuego insertados: " + str(VideoJuego.objects.filter(consola__nombre="Pc").count()))
    print("---------------------------------------------------------")
populateVideoJuegosPc()

def populateVideoJuegosPS4():
    print("Cargando videoJuegos de PS4...")
    VideoJuego.objects.filter(consola__nombre="PS4").delete()
    lista=[]
    listaAux=[]
    listaGeneros=[]
    dict_generos={}
    listaIdJuegos=[]
    fileobj=open(path+"\\datosPs4.txt", "r")
    
 
    i=0
    
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')
        if len(rip) != 7:
            continue
        if  i!=0:
             
                 
            listaString=str(rip[3])
            generos=(listaString.strip()).split(',')
            
            
            listaAux=[]
            for genero in generos:
                listaAux.append(Genero.objects.get(nombre=genero.strip("[ ' ]")))
            listaGeneros.append(listaAux)
           
            u=VideoJuego(nombre=rip[0], precio=rip[1], consola=Consola.objects.get(nombre=rip[2]) ,urlProducto=rip[4], urlImg=rip[5], fechaLanzamiento=datetime.strptime(rip[6],'%d-%m-%Y'))
            lista.append(u)
        i=i+1   
    fileobj.close()
    VideoJuego.objects.bulk_create(lista)
    
    for juegosPS4 in VideoJuego.objects.filter(consola__nombre="PS4"):
                listaIdJuegos.append(juegosPS4.idVideoJuegos)
    
    listaIdJuegos.sort(key=None, reverse=False)
    dict_generos=dict(zip(listaIdJuegos,listaGeneros))
    
    
    
    listaIdJuegos.sort(key=None, reverse=False)
    dict_generos=dict(zip(listaIdJuegos,listaGeneros))
    
    
    dict2={}
   
    for juegosPS4 in VideoJuego.objects.filter(consola__nombre="PS4"):
        juegosPS4.generos.set(dict_generos[juegosPS4.idVideoJuegos])
        dict2[juegosPS4.idVideoJuegos]=juegosPS4
    
    print("Videojuego insertados: " + str(VideoJuego.objects.filter(consola__nombre="PS4").count()))
    print("---------------------------------------------------------")

populateVideoJuegosPS4()

def populateVideoJuegosXboxOne():
    print("Cargando videoJuegos de Xbox One...")
    VideoJuego.objects.filter(consola__nombre="Xbox One").delete()
    lista=[]
    listaAux=[]
    listaGeneros=[]
    dict_generos={}
    listaIdJuegos=[]
    fileobj=open(path+"\\datosXboxOne.txt", "r")
    
 
    i=0
    
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')
        if len(rip) != 7:
            continue
        if  i!=0:
             
                 
            listaString=str(rip[3])
            generos=(listaString.strip()).split(',')
            
            
            listaAux=[]
            for genero in generos:
                listaAux.append(Genero.objects.get(nombre=genero.strip("[ ' ]")))
            listaGeneros.append(listaAux)
           
            u=VideoJuego(nombre=rip[0], precio=rip[1], consola=Consola.objects.get(nombre=rip[2]) ,urlProducto=rip[4], urlImg=rip[5], fechaLanzamiento=datetime.strptime(rip[6],'%d-%m-%Y'))
            lista.append(u)
        i=i+1   
    fileobj.close()
    VideoJuego.objects.bulk_create(lista)
    
    for juegosXboxOne in VideoJuego.objects.filter(consola__nombre="PS4"):
                listaIdJuegos.append(juegosXboxOne.idVideoJuegos)
    
    listaIdJuegos.sort(key=None, reverse=False)
    dict_generos=dict(zip(listaIdJuegos,listaGeneros))
    
    
    
    listaIdJuegos.sort(key=None, reverse=False)
    dict_generos=dict(zip(listaIdJuegos,listaGeneros))
    
    
    dict2={}
   
    for juegosXboxOne in VideoJuego.objects.filter(consola__nombre="XboxOne"):
        juegosXboxOne.generos.set(dict_generos[juegosXboxOne.idVideoJuegos])
        dict2[juegosXboxOne.idVideoJuegos]=juegosXboxOne 
    
    print("Videojuego insertados: " + str(VideoJuego.objects.filter(consola__nombre="XboxOne").count()))
    print("---------------------------------------------------------")



