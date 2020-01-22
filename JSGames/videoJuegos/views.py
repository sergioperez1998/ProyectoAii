#encoding:utf-8
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from videoJuegos.models import Genero, VideoJuego, Consola, Cliente
from django.contrib.auth.decorators import login_required
from django.contrib.auth  import login, authenticate
from videoJuegos.forms import CustomUserForm, ClienteForm, BusquedaPorGeneroForm
from django.contrib.auth.models import User
from twisted.words.protocols.jabber import jstrports
from django.template.defaulttags import ifequal
from random import randint

#path="C:\\Users\\migue\\Desktop\\AII\\ProyectoAii\\JSGames\\data"
#path="C:\\Users\\Usuario\\Desktop\\Universidad\\cuarto año\\AII\\Proyecto git\\ProyectoAii\\JSGames\\data"
#path="C:\\Users\\sergi\\Desktop\\Mi Equipo\\Facultad\\CUARTO CURSO\\ACCESO INTELIGENTE A LA INFORMACION\\PROYECTO AII\\ProyectoAii\\JSGames\\data"
path = "C:\\Users\\sergi\\Desktop\\Datos"
@login_required(login_url='/ingresar')
def populateDatabase(request):
    populateConsola()
    populateGeneros()
    populateVideoJuegosNintendoSwitch()
    populateVideoJuegosPc()
    populateVideoJuegosPS4()
    populateVideoJuegosXboxOne()
     
    idUsuario =request.user.id
    usuarioActual = get_object_or_404(User, pk=idUsuario)
    nombre=usuarioActual.username 
    logout(request)
    return render(request, 'index.html',{ 'nombre':nombre})

@login_required() 
def index(request):
    idUsuario =request.user.id
    usuarioActual = get_object_or_404(User, pk=idUsuario)
    nombre=usuarioActual.username
    
    return render(request, 'master.html',{'STATIC_URL':settings.STATIC_URL, 'nombre':nombre})

def ingresar(request):
    if request.user.is_authenticated:
        return(HttpResponseRedirect('/populate'))
    formulario = AuthenticationForm()
    if request.method=='POST':
        formulario = AuthenticationForm(request.POST)
        usuario=request.POST['username']
        clave=request.POST['password']
        acceso=authenticate(username=usuario,password=clave)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return (HttpResponseRedirect('/populate'))
            else:
                return (HttpResponse('<html><body>ERROR: USUARIO NO ACTIVO </body></html>'))
        else:
            return (HttpResponse('<html><body>ERROR: USUARIO O CONTARSE&Ntilde;A INCORRECTOS </body></html>'))
                     
    return render(request, 'ingresar.html', {'formulario':formulario})



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
    
    for juegosXboxOne in VideoJuego.objects.filter(consola__nombre="Xbox One"):
                listaIdJuegos.append(juegosXboxOne.idVideoJuegos)
    
    listaIdJuegos.sort(key=None, reverse=False)
    dict_generos=dict(zip(listaIdJuegos,listaGeneros))
    
    
    
    listaIdJuegos.sort(key=None, reverse=False)
    dict_generos=dict(zip(listaIdJuegos,listaGeneros))
    
    
    dict2={}
   
    for juegosXboxOne in VideoJuego.objects.filter(consola__nombre="Xbox One"):
        juegosXboxOne.generos.set(dict_generos[juegosXboxOne.idVideoJuegos])
        dict2[juegosXboxOne.idVideoJuegos]=juegosXboxOne 
    
    print("Videojuego insertados: " + str(VideoJuego.objects.filter(consola__nombre="Xbox One").count()))
    print("---------------------------------------------------------")
def populateConsola():
    print("----------------------------------------------")
    
    if Consola.objects.all().exists():
        print("Las consolas ya estaban cargadas")
        print("----------------------------------------------")
       
        
    else:
        print("Cargando las consolas predeterminadas")
        listaConsolas=[]
        nintendoSwitch=Consola(nombre="Nintendo Switch", urlImg="https://images-na.ssl-images-amazon.com/images/I/71ivrWiYkLL._SX466_.jpg", 
                descripcion="Es un híbrido entre portátil y sobremesa con mandos separables."
                " Nintendo acaba de presentar Switch, su nueva consola que mezcla en un "
                "mismo aparato las características de una sobremesa con una portátil. La compañía japonesa ha presentada" 
                "esta nueva máquina a través de un vídeo que muestra su peculiar funcionamiento.")
       
        Pc=Consola(nombre="Pc", urlImg="https://images-na.ssl-images-amazon.com/images/I/51afVSRxJlL._SX466_.jpg", 
                descripcion="Un juego de computadora es un programa que sirve de entretenimiento y que es jugado en una computadora -generalmente una PC- en lugar de consolas y similares")
       
        PS4=Consola(nombre="PS4", urlImg="https://media.playstation.com/is/image/SCEA/playstation-4-pro-vertical-product-shot-01-us-07sep16?$native_t$", 
                descripcion="PS4 es un sistema de entretenimiento digital y la cuarta consola de sobremesa desarrollada por Sony Computer Entertainment.")
        XboxOne=Consola(nombre="Xbox One", urlImg="https://compass-ssl.xbox.com/assets/05/b0/05b01a46-58eb-4927-ad21-3c43b545ebaf.jpg?n=X1S-2019_Panes-2-Up-1084_111_570x400.jpg", 
                descripcion="La consola está formada por un procesador AMD de 8 núcleos Custom de 64 bits basado en microarquitectura Jaguar y una velocidad estimada en 1,75Ghz, 8 GB de memoria RAM DDR3 más 32MB de ESRAM, con una velocidad de hasta 204GB/s​ 500 GB de disco duro y un lector Blu-ray 6x.")
        listaConsolas.append(nintendoSwitch)
        listaConsolas.append(Pc)
        listaConsolas.append(PS4)
        listaConsolas.append(XboxOne)
        
        Consola.objects.bulk_create(listaConsolas)
        print("Consolas cargadas")
        print("----------------------------------------------")
       
def registerView(request):
    if request.method == "POST":
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user= authenticate(username=username, password= password)
            login(request, user)
            return redirect("inicio")
    else:
        form=CustomUserForm()
        
    return render(request,'videoJuegos/cliente_form.html', {"form":form})

def startPage(request):
    return render(request, 'videoJuegos/startPage.html')

def showUser(request):
    
    idUsuario =request.user.id
    usuario = get_object_or_404(User, pk=idUsuario)
    return render(request, 'videoJuegos/showUser.html', {'user':usuario})

def showVideoJuegosCliente(request):
    
    JuegosPc = []
    JuegosNintendo=[]
    JuegosPs4=[]
    JuegosXbox=[]
    idUsuario =request.user.id
    usuarioActual = get_object_or_404(User, pk=idUsuario)
    juegosCliente=[]
    if existeUsuario(usuarioActual)==True:
        cliente = Cliente.objects.get(usuario=usuarioActual)
        for g in cliente.videoJuegos.all():
            juegosCliente.append(g.nombre)
    
    Juegos = VideoJuego.objects.all()
    for j in Juegos:
        if ("Pc" in j.consola.nombre) and (j.nombre not in juegosCliente):
            JuegosPc.append(j)
        if ("Nintendo Switch" in j.consola.nombre) and (j.nombre not in juegosCliente):
            JuegosNintendo.append(j)
        if ("PS4" in j.consola.nombre) and (j.nombre not in juegosCliente):
            JuegosPs4.append(j)
        if ("Xbox One" in j.consola.nombre) and (j.nombre not in juegosCliente):
            JuegosXbox.append(j)
    return render(request, 'videoJuegos/mostrarVideoJuegosCliente.html', 
                  {"juegosPc":JuegosPc, "juegosNintendo":JuegosNintendo, "juegosPs4":JuegosPs4,"juegosXbox":JuegosXbox})

def agregarJuego(request, idVideoJuegos):
    
    #Juego seleccionado y Usuario logueado
    game = VideoJuego.objects.get(idVideoJuegos=idVideoJuegos)
    idUsuario =request.user.id
    usuarioActual = get_object_or_404(User, pk=idUsuario)
    
    if not(Cliente.objects.all().exists()) or existeUsuario(usuarioActual)==False:
        juegosCliente=[]
        consolasCliente=[]
        juegosCliente.append(game)
        consolasCliente.append(game.consola)
        nuevoCliente = Cliente.objects.create(usuario=usuarioActual)
        nuevoCliente.consolas.add(game.consola)
        nuevoCliente.videoJuegos.add(game)
    else:
        cliente = Cliente.objects.get(usuario=usuarioActual)
        cliente.videoJuegos.add(game)
        if not(game.consola in cliente.consolas.all()):
            cliente.consolas.add(game.consola)    
    return redirect(to="showGames_url")


#Metodo para verificar que el usuario existe como cliente en BD          
def existeUsuario(usuario):
    existe=False
    Clientes=Cliente.objects.all()
    for c in Clientes:
        usuarioCliente = c.usuario
        if usuario == usuarioCliente:
            existe =True
    return existe      

def showConsolasCliente(request):
    
    idUsuario =request.user.id
    usuarioActual = get_object_or_404(User, pk=idUsuario)
    consolasCliente=[]
    if existeUsuario(usuarioActual)==True:
        cliente = Cliente.objects.get(usuario=usuarioActual)
        consolasCliente=cliente.consolas.all()
    

    return render(request, 'videoJuegos/mostrarConsolasDelCliente.html',{"consolasCliente":consolasCliente})
def showVideoJuegosDelCliente(request, nombre):
    
    idUsuario =request.user.id
    usuarioActual = get_object_or_404(User, pk=idUsuario)
    videojuegosCliente=[]
    if existeUsuario(usuarioActual)==True:
        cliente = Cliente.objects.get(usuario=usuarioActual)
        videoJuegosCliente=cliente.videoJuegos.filter(consola__nombre=nombre)
    

    return render(request, 'videoJuegos/mostrarVideoJuegosDelCliente.html',{"videoJuegosCliente":videoJuegosCliente})        
                   
def eliminarJuego(request, idVideoJuegos, buscar):
    listaJuegosCliente=[]
    #Juego seleccionado y Usuario logueado
    game = VideoJuego.objects.get(idVideoJuegos=idVideoJuegos)
    
    nombre=game.consola.nombre
    idUsuario =request.user.id
    usuarioActual = get_object_or_404(User, pk=idUsuario)
    cliente = Cliente.objects.get(usuario=usuarioActual)
    cliente.videoJuegos.remove(game)
    
    
    
    videoJuegosCliente=cliente.videoJuegos.filter(consola__nombre=nombre)
    
    if 'nobuscar' in buscar:    
        return render(request, 'videoJuegos/mostrarVideoJuegosDelCliente.html',{"videoJuegosCliente":videoJuegosCliente})  
    else:
        return render(request, 'index.html',{})  
                
def mostrar_videoJuegos_genero(request):
    formulario = BusquedaPorGeneroForm()
    
    genero=None
    cadenaNombre=''
    cadena=''
    generos=Genero.objects.all()
    for g in generos:
        cadena=cadena + g.nombre+ ", "
        
    cadenaNombre = '( ' +cadena[2:-2]+' )' 
        
    try:
        if request.method=='POST':
            formulario = BusquedaPorGeneroForm(request.POST)
          
             
            if formulario.is_valid():
                videoJuegos=VideoJuego.objects.all()
                nombreGenero=formulario.cleaned_data['genero']
                genero = Genero.objects.get(nombre=nombreGenero.capitalize())
                videoJuegos = videoJuegos.filter(generos=genero)
                print(videoJuegos)
               
                     
              
        else:
            videoJuegos=VideoJuego.objects.all()
        
        if videoJuegos.exists():    
            return render(request, 'videoJuegos/mostrarVideoJuegosDelCliente2.html', {'formulario':formulario, 'videoJuegos':videoJuegos, 'cadena':cadenaNombre})
        
        else:
            print('estoy aqui')
            aviso='No se han encontrado videojuegos con ' + formulario.cleaned_data['genero'] 
            return render(request, 'videoJuegos/mostrarVideoJuegosDelCliente2.html', {'formulario':formulario, 'videoJuegos':videoJuegos, 'cadena':cadenaNombre, 'aviso':aviso})
        
    except:
        videoJuegos=[]
        aviso='No se han encontrado videojuegos con ' + formulario.cleaned_data['genero'] 
        return render(request, 'videoJuegos/mostrarVideoJuegosDelCliente2.html', {'formulario':formulario, 'videoJuegos':videoJuegos, 'cadena':cadenaNombre, 'aviso':aviso})

def mostrarVideoJuego(request, idVideoJuegos, buscar):
    
    #Juego seleccionado y Usuario logueado
    listaGeneros=[]
    todoUno = ""
    
    videoJuego = VideoJuego.objects.get(idVideoJuegos=idVideoJuegos)
    consola=videoJuego.consola.nombre
    print(consola)
    
    for genero in videoJuego.generos.all():
        
        listaGeneros.append(genero.nombre)
        todoUno=str(todoUno)+ str(genero.nombre) +", "
        
        
    generos = todoUno[:-2]
    

   
    
    return render(request, 'videoJuegos/mostrarVideoJuego.html',{"videoJuego":videoJuego,'generos':generos, 'consola':consola, 'buscar':buscar})  




def mostrarVideoJuegoAgregar(request, idVideoJuegos):
    
    #Juego seleccionado y Usuario logueado
    
    todoUno = ""
    
    videoJuego = VideoJuego.objects.get(idVideoJuegos=idVideoJuegos)
    
    for genero in videoJuego.generos.all():
        
        
        todoUno=str(todoUno)+ str(genero.nombre) +", "
        
        
    generos = todoUno[:-2]
    

   
    
    return render(request, 'videoJuegos/mostrarVideoJuego.html',{"videoJuego":videoJuego,'generos':generos})

def recomendarVideojuegos(request):

    idUsuario = request.user.id
    usuarioActual = get_object_or_404(User, pk=idUsuario)
    generosCliente = []
    juegosCliente = []
    juegosARecomendar = []
    recomendacion = []
    boolean = True
    if existeUsuario(usuarioActual)==True:
        cliente = Cliente.objects.get(usuario=usuarioActual)

        if not cliente.videoJuegos.all():
            return redirect(to="showGames_url")
        
        for v in cliente.videoJuegos.all():
            juegosCliente.append(v)
            for g in v.generos.all():
                if g not in generosCliente:
                    generosCliente.append(g)

        for v in VideoJuego.objects.all():
            for g in v.generos.all():
                if g in generosCliente:
                    if v not in juegosARecomendar:
                        juegosARecomendar.append(v)

        for v in juegosCliente:
            juegosARecomendar.remove(v)
        if len(juegosARecomendar)>5:
            numero1 = randint(0, len(juegosARecomendar)-1)
            numero2 = randint(0, len(juegosARecomendar)-1)
            numero3 = randint(0, len(juegosARecomendar)-1)
            numero4 = randint(0, len(juegosARecomendar)-1)
            numero5 = randint(0, len(juegosARecomendar)-1)

            recomendacion.append(juegosARecomendar[numero1])
            if juegosARecomendar[numero2] not in recomendacion:
                recomendacion.append(juegosARecomendar[numero2])
            if juegosARecomendar[numero3] not in recomendacion:
                recomendacion.append(juegosARecomendar[numero3])
            if juegosARecomendar[numero4] not in recomendacion:
                recomendacion.append(juegosARecomendar[numero4])
            if juegosARecomendar[numero5] not in recomendacion:
                recomendacion.append(juegosARecomendar[numero5])

            return render(request, 'videoJuegos/recomendacion.html',{"recomendacion":recomendacion, "cliente":cliente, "boolean":boolean})
            
        else:
            return render(request, 'videoJuegos/recomendacion.html',{"recomendacion":juegosARecomendar, "cliente":cliente, "boolean":boolean})
    else:
        return redirect(to="showGames_url")  









