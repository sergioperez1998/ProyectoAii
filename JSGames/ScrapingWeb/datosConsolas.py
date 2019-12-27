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

def datosConsolas():

    
    urlConsolas = "https://www.game.es/VIDEOJUEGOS/CONSOLAS"
    
    req = Request(urlConsolas, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(urlopen(req).read().decode("latin-1"), 'html.parser')  

    listado_url=[]
    for secciones in soup.findAll("h2",attrs={"class":"section-title"}):
        url=secciones.a.get("href")
        url_parseadas=eliminadorDiacriticos(url)
        listado_url.append(url_parseadas)

    #Url de las consolas
    urlNintendoSwitch="https://www.game.es"+listado_url[0].split("/")[0]+"/"+listado_url[0].split("/")[1]+"/"+ listado_url[0].split("/")[2]+"/"
    urlPS4="https://www.game.es"+listado_url[1].split("/")[0]+"/"+listado_url[1].split("/")[1]+"/"+ listado_url[1].split("/")[2]+"/"
    urlXboxOne="https://www.game.es"+listado_url[2]
    urlPc="https://www.game.es/buscar/ordenadores/"

    req1 = Request(urlNintendoSwitch, headers={'User-Agent': 'Mozilla/5.0'})
    soup1 = BeautifulSoup(urlopen(req1).read().decode("latin-1"), 'html.parser')

    for div in soup1.findAll("div",attrs={"id":"searchItemsWrap"}):
        for div1 in div.findAll("div",attrs={"class":"search-item"}):
            print(div1.a)




datosConsolas()