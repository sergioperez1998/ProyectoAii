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

def datosJuegosPc():

    urlBasica="https://www.eneba.com"
    urlJuegosPc = "https://www.eneba.com/es/store?page=1&platforms[]=STEAM&types[]=game"

    month = {	'Janauary':'01',
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

def datosJuegosXboxOne():

    urlBasica="https://www.eneba.com"

    urlJuegosXboxOne="https://www.eneba.com/es/store?page=1&platforms[]=XBOX&types[]=game"

    month = {	'Janauary':'01',
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

def datosJuegosNintendoSwitch():

    urlBasica="https://www.eneba.com"

    urlJuegosNintendoSwitch="https://www.eneba.com/es/store?page=1&platforms[]=NINTENDO&types[]=game"
    #urlJuegosPS4 = "https://www.eneba.com/es/store/psn-games"

    month = {	'Janauary':'01',
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

    urlJuegosPS4 = "https://www.eneba.com/es/store/psn-games"

    month = {	'Janauary':'01',
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
    listadoPreciosJuegosSwitchPs4=[]
    listadoGenerosJuegoPs4Total=[]
    listadoGenerosPagina=[]
    listadoFechaLanzamientoJuegoPs4=[]


datosJuegosPs4()