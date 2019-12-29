from datetime import datetime as datetime2
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
import datetime
import os, os.path
from unicodedata import normalize
import errno
from urllib.request import Request, urlopen
import re

def eliminadorDiacriticos(cadena):
    
    s = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
    normalize("NFD", cadena), 0, re.I)
    s = normalize('NFC', s)
    return s

def multiPaginaJuegosPc():
    
    i=1
    numeroPaginas=2

    diccionario={
       "Nombres":{},
        "Precios":{},
        "Plataforma":"Pc",
        "Generos":{},
        "Url":{},
        "Imagenes":{},
        "FechaLanzamiento":{},
        "GenerosPagina":{}
    }
    
    while i<numeroPaginas+1:

        url="https://www.eneba.com/es/store?page="+str(i)+"&platforms[]=STEAM&types[]=game"
        if i == 1:
            diccionario=datosJuegosPc(url)
        else:
            diccionario["Nombres"].extend(datosJuegosPc(url)["Nombres"])
            diccionario["Precios"].extend(datosJuegosPc(url)["Precios"])
            diccionario["Generos"].extend(datosJuegosPc(url)["Generos"])
            diccionario["Url"].extend(datosJuegosPc(url)["Url"])
            diccionario["Imagenes"].extend(datosJuegosPc(url)["Imagenes"])
            diccionario["FechaLanzamiento"].extend(datosJuegosPc(url)["FechaLanzamiento"])
            lista=diccionario["GenerosPagina"]
            for genero in datosJuegosPc(url)["GenerosPagina"]:
                if genero not in lista:
                    lista.append(genero)
                    diccionario["GenerosPagina"] = lista
        i=i+1

    return diccionario


def datosJuegosPc(urlJuegosPc):

    urlBasica="https://www.eneba.com"


    month = {	'January':'01',
		'February':'02',
		'March':'03',
		'April':'04',
		'May':'05',
		'June':'06',
		'July':'07',
		'August':'08',
		'September':'09',
		'October':'10',
		'November':'11',
		'December':'12'		}

    reqPc = Request(urlJuegosPc, headers={'User-Agent': 'Mozilla/5.0'})
    soupPc = BeautifulSoup(urlopen(reqPc).read().decode("latin-1"), 'html.parser')  

    listadoNombresJuegosPc=[]
    listadoImagenesJuegosPc=[]
    listadoUrlJuegosPc=[]
    listadoPreciosJuegosPcActual=[]
    listadoGenerosJuegoPcTotal=[]
    listadoGenerosPagina=[]
    listadoFechaLanzamientoJuegoPc=[]

    for juegos in soupPc.find_all("div", attrs={"class":"_3M7T08"}):
        for juego in juegos.find_all("div", attrs={"class":"_2rxjGA"}):
            for datos1 in juego.find_all("div", attrs={"class":"_3shANq"}):
                for nombre in datos1.find_all("div", attrs={"class":"_1ZwRcm"}):
                    nombreJuego=nombre.span.get_text()
                    nombreJuegoSerializado= eliminadorDiacriticos(nombreJuego)
                    listadoNombresJuegosPc.append(nombreJuegoSerializado)
                for img in datos1.find_all("div", attrs={"class":"_2vZ2Ja _1p1I8b"}):
                    imagenJuego=img.img.get("src")
                    imagenJuegoSerializada = eliminadorDiacriticos(imagenJuego)
                    listadoImagenesJuegosPc.append(imagenJuegoSerializada)
            for datos2 in juego.find_all("div", attrs={"class":"_12ISZC"}):
                for url in datos2.find_all("a", attrs={"class":"_2idjXd"}):
                    urlJuego=urlBasica + url.get("href")
                    listadoUrlJuegosPc.append(urlJuego)

    for juegoPc in listadoUrlJuegosPc:

        reqJuegoPc = Request(juegoPc, headers={'User-Agent': 'Mozilla/5.0'})
        soupJuegoPC = BeautifulSoup(urlopen(reqJuegoPc).read().decode("latin-1"), 'html.parser')

        precioJuegoAhora= soupJuegoPC.find("span", attrs={"class":"_1fTsyE"})
        if "NoneType" in type(precioJuegoAhora).__name__:
            precioJuegoPcAhora = "Agotado"
        else:
            precioJuegoPcAhora = precioJuegoAhora.get_text().split("¬")[1]
        listadoPreciosJuegosPcActual.append(precioJuegoPcAhora)

        for generos in soupJuegoPC.find_all("ul", attrs={"class":"_3w9_g5"}):
            listadoGenerosJuegoPc=[]
            for generosJuegos in generos.find_all("li"):
                genero=generosJuegos.a.get_text()
                generoSerializado=eliminadorDiacriticos(genero)
                if "A³" in generoSerializado:
                    generoSerializado="Accion"
                listadoGenerosJuegoPc.append(generoSerializado)
                if not(generoSerializado in listadoGenerosPagina):
                    listadoGenerosPagina.append(generoSerializado)
            listadoGenerosJuegoPcTotal.append(listadoGenerosJuegoPc)

        fechaLanzamiento = soupJuegoPC.find("p", attrs={"class":"FpVQmt"})
        fechaLanzamientoJuegoPc=(fechaLanzamiento.get_text().split(" ")[1].strip(",")+"-"
            +month[fechaLanzamiento.get_text().split(" ")[0]]+"-"+fechaLanzamiento.get_text().split(" ")[2])
        listadoFechaLanzamientoJuegoPc.append(fechaLanzamientoJuegoPc)

    contenidoJuegosPc = {
        "Nombres":listadoNombresJuegosPc,
        "Precios":listadoPreciosJuegosPcActual,
        "Plataforma":"Pc",
        "Generos":listadoGenerosJuegoPcTotal,
        "Url":listadoUrlJuegosPc,
        "Imagenes":listadoImagenesJuegosPc,
        "FechaLanzamiento":listadoFechaLanzamientoJuegoPc,
        "GenerosPagina":listadoGenerosPagina
    }

    return contenidoJuegosPc

def multiPaginaJuegosXboxOne():
    
    i=1
    numeroPaginas=2

    diccionario={
       "Nombres":{},
        "Precios":{},
        "Plataforma":"Pc",
        "Generos":{},
        "Url":{},
        "Imagenes":{},
        "FechaLanzamiento":{},
        "GenerosPagina":{}
    }
    
    while i<numeroPaginas+1:

        url="https://www.eneba.com/es/store?page="+str(i)+"&platforms[]=XBOX&types[]=game"
        if i == 1:
            diccionario=datosJuegosXboxOne(url)
        else:
            diccionario["Nombres"].extend(datosJuegosXboxOne(url)["Nombres"])
            diccionario["Precios"].extend(datosJuegosXboxOne(url)["Precios"])
            diccionario["Generos"].extend(datosJuegosXboxOne(url)["Generos"])
            diccionario["Url"].extend(datosJuegosXboxOne(url)["Url"])
            diccionario["Imagenes"].extend(datosJuegosXboxOne(url)["Imagenes"])
            diccionario["FechaLanzamiento"].extend(datosJuegosXboxOne(url)["FechaLanzamiento"])
            lista=diccionario["GenerosPagina"]
            for genero in datosJuegosXboxOne(url)["GenerosPagina"]:
                if genero not in lista:
                    lista.append(genero)
                    diccionario["GenerosPagina"] = lista
        i=i+1

    return diccionario

def datosJuegosXboxOne(urlJuegosXboxOne):

    urlBasica="https://www.eneba.com"

    month = {	'January':'01',
		'February':'02',
		'March':'03',
		'April':'04',
		'May':'05',
		'June':'06',
		'July':'07',
		'August':'08',
		'September':'09',
		'October':'10',
		'November':'11',
		'December':'12'		}

    reqXbox = Request(urlJuegosXboxOne, headers={'User-Agent': 'Mozilla/5.0'})
    soupXbox = BeautifulSoup(urlopen(reqXbox).read().decode("latin-1"), 'html.parser')

    listadoNombresJuegosXboxOne=[]
    listadoImagenesJuegosXboxOne=[]
    listadoUrlJuegosXboxOne=[]
    listadoPreciosJuegosXboxOneActual=[]
    listadoGenerosJuegoXboxTotal=[]
    listadoGenerosPagina=[]
    listadoFechaLanzamientoJuegoXboxOne=[]

    for juegos in soupXbox.find_all("div", attrs={"class":"_3M7T08"}):
        for juego in juegos.find_all("div", attrs={"class":"_2rxjGA"}):
            for datos1 in juego.find_all("div", attrs={"class":"_3shANq"}):
                for nombre in datos1.find_all("div", attrs={"class":"_1ZwRcm"}):
                    nombreJuego=nombre.span.get_text()
                    nombreJuegoSerializado= eliminadorDiacriticos(nombreJuego)
                    listadoNombresJuegosXboxOne.append(nombreJuegoSerializado)
                for img in datos1.find_all("div", attrs={"class":"_2vZ2Ja _1p1I8b"}):
                    imagenJuego=img.img.get("src")
                    imagenJuegoSerializada = eliminadorDiacriticos(imagenJuego)
                    listadoImagenesJuegosXboxOne.append(imagenJuegoSerializada)
            for datos2 in juego.find_all("div", attrs={"class":"_12ISZC"}):
                for url in datos2.find_all("a", attrs={"class":"_2idjXd"}):
                    urlJuego=urlBasica + url.get("href")
                    listadoUrlJuegosXboxOne.append(urlJuego)

    for juegoXboxOne in listadoUrlJuegosXboxOne:

        reqJuegoXboxOne = Request(juegoXboxOne, headers={'User-Agent': 'Mozilla/5.0'})
        soupJuegoXboxOne = BeautifulSoup(urlopen(reqJuegoXboxOne).read().decode("latin-1"), 'html.parser')

        precioJuegoAhora= soupJuegoXboxOne.find("span", attrs={"class":"_1fTsyE"})
        if "NoneType" in type(precioJuegoAhora).__name__:
            precioJuegoXboxOneAhora = "Agotado"
        else:
            precioJuegoXboxOneAhora = precioJuegoAhora.get_text().split("¬")[1]
        listadoPreciosJuegosXboxOneActual.append(precioJuegoXboxOneAhora)

        for generos in soupJuegoXboxOne.find_all("ul", attrs={"class":"_3w9_g5"}):
            listadoGenerosJuegoXboxOne=[]
            for generosJuegos in generos.find_all("li"):
                genero=generosJuegos.a.get_text()
                generoSerializado=eliminadorDiacriticos(genero)
                if "A³" in generoSerializado:
                    generoSerializado="Accion"
                listadoGenerosJuegoXboxOne.append(generoSerializado)
                if not(generoSerializado in listadoGenerosPagina):
                    listadoGenerosPagina.append(generoSerializado)
            listadoGenerosJuegoXboxTotal.append(listadoGenerosJuegoXboxOne)
        
        fechaLanzamiento = soupJuegoXboxOne.find("p", attrs={"class":"FpVQmt"})
        fechaLanzamientoJuegoXboxOne=(fechaLanzamiento.get_text().split(" ")[1].strip(",")+"-"
            +month[fechaLanzamiento.get_text().split(" ")[0]]+"-"+fechaLanzamiento.get_text().split(" ")[2])
        listadoFechaLanzamientoJuegoXboxOne.append(fechaLanzamientoJuegoXboxOne)

    contenidoJuegosXbox = {
        "Nombres":listadoNombresJuegosXboxOne,
        "Precios":listadoPreciosJuegosXboxOneActual,
        "Plataforma":"Xbox One",
        "Generos":listadoGenerosJuegoXboxTotal,
        "Url":listadoUrlJuegosXboxOne,
        "Imagenes":listadoImagenesJuegosXboxOne,
        "FechaLanzamiento":listadoFechaLanzamientoJuegoXboxOne,
        "GenerosPagina":listadoGenerosPagina
    }

    return contenidoJuegosXbox

def multiPaginaJuegosNintendoSwitch():
    
    i=1
    numeroPaginas=2

    diccionario={
       "Nombres":{},
        "Precios":{},
        "Plataforma":"Pc",
        "Generos":{},
        "Url":{},
        "Imagenes":{},
        "FechaLanzamiento":{},
        "GenerosPagina":{}
    }
    
    while i<numeroPaginas+1:

        url="https://www.eneba.com/es/store?page="+str(i)+"&platforms[]=NINTENDO&types[]=game"
        if i == 1:
            diccionario=datosJuegosNintendoSwitch(url)
        else:
            diccionario["Nombres"].extend(datosJuegosNintendoSwitch(url)["Nombres"])
            diccionario["Precios"].extend(datosJuegosNintendoSwitch(url)["Precios"])
            diccionario["Generos"].extend(datosJuegosNintendoSwitch(url)["Generos"])
            diccionario["Url"].extend(datosJuegosNintendoSwitch(url)["Url"])
            diccionario["Imagenes"].extend(datosJuegosNintendoSwitch(url)["Imagenes"])
            diccionario["FechaLanzamiento"].extend(datosJuegosNintendoSwitch(url)["FechaLanzamiento"])
            lista=diccionario["GenerosPagina"]
            for genero in datosJuegosNintendoSwitch(url)["GenerosPagina"]:
                if genero not in lista:
                    lista.append(genero)
                    diccionario["GenerosPagina"] = lista
        i=i+1

    return diccionario

def datosJuegosNintendoSwitch(urlJuegosNintendoSwitch):

    urlBasica="https://www.eneba.com"

    month = {	'January':'01',
		'February':'02',
		'March':'03',
		'April':'04',
		'May':'05',
		'June':'06',
		'July':'07',
		'August':'08',
		'September':'09',
		'October':'10',
		'November':'11',
		'December':'12'		}

    reqSwitch = Request(urlJuegosNintendoSwitch, headers={'User-Agent': 'Mozilla/5.0'})
    soupSwitch = BeautifulSoup(urlopen(reqSwitch).read().decode("latin-1"), 'html.parser')

    listadoNombresJuegosSwitch=[]
    listadoImagenesJuegosSwitch=[]
    listadoUrlJuegosSwitch=[]
    listadoPreciosJuegosSwitchActual=[]
    listadoGenerosJuegoSwitchTotal=[]
    listadoGenerosPagina=[]
    listadoFechaLanzamientoJuegoSwitch=[]

    for juegos in soupSwitch.find_all("div", attrs={"class":"_3M7T08"}):
        for juego in juegos.find_all("div", attrs={"class":"_2rxjGA"}):
            for datos1 in juego.find_all("div", attrs={"class":"_3shANq"}):
                for nombre in datos1.find_all("div", attrs={"class":"_1ZwRcm"}):
                    nombreJuego=nombre.span.get_text()
                    nombreJuegoSerializado= eliminadorDiacriticos(nombreJuego)
                    listadoNombresJuegosSwitch.append(nombreJuegoSerializado)
                for img in datos1.find_all("div", attrs={"class":"_2vZ2Ja _1p1I8b"}):
                    imagenJuego=img.img.get("src")
                    imagenJuegoSerializada = eliminadorDiacriticos(imagenJuego)
                    listadoImagenesJuegosSwitch.append(imagenJuegoSerializada)
            for datos2 in juego.find_all("div", attrs={"class":"_12ISZC"}):
                for url in datos2.find_all("a", attrs={"class":"_2idjXd"}):
                    urlJuego=urlBasica + url.get("href")
                    listadoUrlJuegosSwitch.append(urlJuego)

    for juegoSwitch in listadoUrlJuegosSwitch:

        reqJuegoSwitch = Request(juegoSwitch, headers={'User-Agent': 'Mozilla/5.0'})
        soupJuegoSwitch = BeautifulSoup(urlopen(reqJuegoSwitch).read().decode("latin-1"), 'html.parser')

        precioJuegoAhora= soupJuegoSwitch.find("span", attrs={"class":"_1fTsyE"})
        if "NoneType" in type(precioJuegoAhora).__name__:
            precioJuegoSwitchAhora = "Agotado"
        else:
            precioJuegoSwitchAhora = precioJuegoAhora.get_text().split("¬")[1]
        listadoPreciosJuegosSwitchActual.append(precioJuegoSwitchAhora)

        for generos in soupJuegoSwitch.find_all("ul", attrs={"class":"_3w9_g5"}):
            listadoGenerosJuegoSwitch=[]
            for generosJuegos in generos.find_all("li"):
                genero=generosJuegos.a.get_text()
                generoSerializado=eliminadorDiacriticos(genero)
                if "A³" in generoSerializado:
                    generoSerializado="Accion"
                listadoGenerosJuegoSwitch.append(generoSerializado)
                if not(generoSerializado in listadoGenerosPagina):
                    listadoGenerosPagina.append(generoSerializado)
            listadoGenerosJuegoSwitchTotal.append(listadoGenerosJuegoSwitch)
        
        fechaLanzamiento = soupJuegoSwitch.find("p", attrs={"class":"FpVQmt"})
        fechaLanzamientoJuegoSwitch=(fechaLanzamiento.get_text().split(" ")[1].strip(",")+"-"
            +month[fechaLanzamiento.get_text().split(" ")[0]]+"-"+fechaLanzamiento.get_text().split(" ")[2])
        listadoFechaLanzamientoJuegoSwitch.append(fechaLanzamientoJuegoSwitch)

    contenidoJuegosSwitch = {
        "Nombres":listadoNombresJuegosSwitch,
        "Precios":listadoPreciosJuegosSwitchActual,
        "Plataforma":"Nintendo Switch",
        "Generos":listadoGenerosJuegoSwitchTotal,
        "Url":listadoUrlJuegosSwitch,
        "Imagenes":listadoImagenesJuegosSwitch,
        "FechaLanzamiento":listadoFechaLanzamientoJuegoSwitch,
        "GenerosPagina":listadoGenerosPagina
    }

    return contenidoJuegosSwitch

def datosJuegosPs4():

    urlBasica="https://www.eneba.com"

    urlJuegosPS4 = "https://www.eneba.com/es/store?page=1&platforms[]=PSN&types[]=game"

    month = {	'January':'01',
		'February':'02',
		'March':'03',
		'April':'04',
		'May':'05',
		'June':'06',
		'July':'07',
		'August':'08',
		'September':'09',
		'October':'10',
		'November':'11',
		'December':'12'		}

    reqPs4 = Request(urlJuegosPS4, headers={'User-Agent': 'Mozilla/5.0'})
    soupPs4 = BeautifulSoup(urlopen(reqPs4).read().decode("latin-1"), 'html.parser')

    listadoNombresJuegosPs4=[]
    listadoImagenesJuegosPs4=[]
    listadoUrlJuegosPs4=[]
    listadoPreciosJuegosPs4=[]
    listadoGenerosJuegoPs4Total=[]
    listadoGenerosPagina=[]
    listadoFechaLanzamientoJuegoPs4=[]

    for juegos in soupPs4.find_all("div", attrs={"class":"_3M7T08"}):
        for juego in juegos.find_all("div", attrs={"class":"_2rxjGA"}):
            for datos1 in juego.find_all("div", attrs={"class":"_3shANq"}):
                for nombre in datos1.find_all("div", attrs={"class":"_1ZwRcm"}):
                    nombreJuego=nombre.span.get_text()
                    nombreJuegoSerializado= eliminadorDiacriticos(nombreJuego)
                    listadoNombresJuegosPs4.append(nombreJuegoSerializado)
                for img in datos1.find_all("div", attrs={"class":"_2vZ2Ja _1p1I8b"}):
                    imagenJuego=img.img.get("src")
                    imagenJuegoSerializada = eliminadorDiacriticos(imagenJuego)
                    listadoImagenesJuegosPs4.append(imagenJuegoSerializada)
            for datos2 in juego.find_all("div", attrs={"class":"_12ISZC"}):
                for url in datos2.find_all("a", attrs={"class":"_2idjXd"}):
                    urlJuego=urlBasica + url.get("href")
                    listadoUrlJuegosPs4.append(urlJuego)

    for juegoPs4 in listadoUrlJuegosPs4:

        reqJuegoPs4 = Request(juegoPs4, headers={'User-Agent': 'Mozilla/5.0'})
        soupJuegoPs4 = BeautifulSoup(urlopen(reqJuegoPs4).read().decode("latin-1"), 'html.parser')

        precioJuegoAhora= soupJuegoPs4.find("span", attrs={"class":"_1fTsyE"})
        if "NoneType" in type(precioJuegoAhora).__name__:
            precioJuegoPs4Ahora = "Agotado"
        else:
            precioJuegoPs4Ahora = precioJuegoAhora.get_text().split("¬")[1]
        listadoPreciosJuegosPs4.append(precioJuegoPs4Ahora)

        for generos in soupJuegoPs4.find_all("ul", attrs={"class":"_3w9_g5"}):
            listadoGenerosJuegoPs4=[]
            for generosJuegos in generos.find_all("li"):
                genero=generosJuegos.a.get_text()
                generoSerializado=eliminadorDiacriticos(genero)
                if "A³" in generoSerializado:
                    generoSerializado="Accion"
                listadoGenerosJuegoPs4.append(generoSerializado)
                if not(generoSerializado in listadoGenerosPagina):
                    listadoGenerosPagina.append(generoSerializado)
            listadoGenerosJuegoPs4Total.append(listadoGenerosJuegoPs4)

        fechaLanzamiento = soupJuegoPs4.find("p", attrs={"class":"FpVQmt"})
        fechaLanzamientoJuegoPs4=(fechaLanzamiento.get_text().split(" ")[1].strip(",")+"-"
            +month[fechaLanzamiento.get_text().split(" ")[0]]+"-"+fechaLanzamiento.get_text().split(" ")[2])
        listadoFechaLanzamientoJuegoPs4.append(fechaLanzamientoJuegoPs4)

    contenidoJuegosPs4 = {
        "Nombres":listadoNombresJuegosPs4,
        "Precios":listadoPreciosJuegosPs4,
        "Plataforma":"PS4",
        "Generos":listadoGenerosJuegoPs4Total,
        "Url":listadoUrlJuegosPs4,
        "Imagenes":listadoImagenesJuegosPs4,
        "FechaLanzamiento":listadoFechaLanzamientoJuegoPs4,
        "GenerosPagina":listadoGenerosPagina
    }        

    return contenidoJuegosPs4

def crearTxtJuegosPs4():

    diccionario = datosJuegosPs4()

    try:
        os.mkdir('template')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    file_object = open("template\\datosPs4.txt","w",encoding="utf-8")
    for i in range(0,len(diccionario["Nombres"])):

        if (i+1)%7 ==0:
            file_object.write("\n")
            file_object.write(str(diccionario["Nombres"][i])+"|"+str(diccionario["Precios"][i])+"|"+str(diccionario["Plataforma"][i])+"|"+
                str(diccionario["Generos"][i])+"|"+str(diccionario["Url"][i])+"|"+str(diccionario["Imagenes"][i])+"|"+
                str(diccionario["FechaLanzamiento"][i]))
        else:
            file_object.write(str(diccionario["Nombres"][i])+"|"+str(diccionario["Precios"][i])+"|"+str(diccionario["Plataforma"][i])+"|"+
                str(diccionario["Generos"][i])+"|"+str(diccionario["Url"][i])+"|"+str(diccionario["Imagenes"][i])+"|"+
                str(diccionario["FechaLanzamiento"][i]))

crearTxtJuegosPs4()