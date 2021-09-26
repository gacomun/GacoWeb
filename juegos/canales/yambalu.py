import logging
import requests
from bs4 import BeautifulSoup
import re

# Create a logger for this file
logger = logging.getLogger(__file__)

def tratar_title(cadena):
    cadena=cadena.replace("- Nintendo Switch","")
    cadena=cadena.replace("- PlayStation 4","")
    cadena=cadena.replace("- PlayStation 5","")
    cadena=cadena.rstrip()
    return cadena

def search(title=""):
    return {}

def detail(title=""):
    r = requests.get(title)
    soup = BeautifulSoup(r.text, 'lxml')
    titulo = soup.find('h1').text
    regex = re.compile('caratula_juego.*')
    thumb=soup.find("div", {"class" : regex}).find("img").attrs["src"]
    regex = re.compile('juego_plataforma.*')
    consola=soup.find("div", {"class" : regex}).find("img").attrs["src"]
    consola=consola.replace(".svg","").replace("/img/icons/icon-","")
    lprecios = soup.find('ul',id="precios_block").find_all("li")
    precios={}
    precios['precios'] = []

    for precio in lprecios:
        regex = re.compile('logo_tienda_.*')
        tienda=precio.find("div", {"class" : regex}).attrs['class'][0]
        canal = tienda.replace("logo_tienda_", "")
        regex = re.compile('.*badge-info.*')
        precio=precio.find("div", {"class" : regex}).text
        precio = precio.replace("\n", "")
        precio = precio.replace("'", ".")
        precio = precio.replace("€", "")
        precios['precios'].append({
            'canal': canal,
            'precio': float(precio)
        })

    data = {
        "title":titulo,
        "thumb":thumb,
        "consola":consola,
        'precios':precios['precios']
    }
    return(data)

def ofertas(consola=""):
    ofertas={}
    ofertas['lista'] = []
    if consola=="ps5" or consola=="":
        next="https://www.yambalu.com/index.php?lang=es&bluray=0&checkAccesorios=0&checkConsolas=0&checkBlurays=0&q=&accion=baja-precio&filtro=0&plataforma[]=PS5&checkJuegos=1&page="
        filtro=""
        ofertas=trataPagina(next,filtro,"ps5",ofertas)
    if consola=="ps4" or consola=="":
        next="https://www.yambalu.com/index.php?lang=es&bluray=0&checkAccesorios=0&checkConsolas=0&checkBlurays=0&q=&accion=baja-precio&filtro=0&plataforma[]=PS4&checkJuegos=1&page="
        filtro=""
        ofertas=trataPagina(next,filtro,"ps4",ofertas)
    if consola=="nsw" or consola=="":
        next="https://www.yambalu.com/index.php?lang=es&bluray=0&checkAccesorios=0&checkConsolas=0&checkBlurays=0&q=&accion=baja-precio&filtro=0&plataforma[]=SWITCH&checkJuegos=1&page="
        filtro=""
        ofertas=trataPagina(next,filtro,"nsw",ofertas)
       
    return ofertas

def trataPagina(url,filtro,consola,ofertas):
    page=1
    next =url+str(page)
    while next != "":
        r = requests.get(next)
        soup = BeautifulSoup(r.text, 'lxml')
        juegos = soup.find_all('article')
        for juego in juegos:
            if juego.find("div",class_="new_precio") is not None:
                regex = re.compile('card panel_juego_listado.*')
                titulo=juego.find("div", {"class" : regex}).find("a").attrs["title"]
                precio=juego.find("div",class_="new_precio").text
                precio = precio.replace("\n", "")
                precio = precio.replace("'", ".")
                precio = precio.replace("€", "")
                regex = re.compile('card-image-container.*')
                imagen=juego.find("div", {"class" : regex}).find("img").attrs["data-src"]
                regex = re.compile('item_listado_precio.*')
                descuento=juego.find("small", {"class" : regex}).text
                descuento = descuento.replace("-", "")
                descuento = descuento.replace("%", "")
                urldetalle = "https://www.yambalu.com"+juego.find('a').attrs['href']
                # detalles=detail(urldetalle)
                # for oferta in detalles["precios"]:

                ofertas['lista'].append({
                    'titulo': tratar_title(titulo),
                    'thumb':imagen,
                    'detail': urldetalle,
                    'precio':float(precio),
                    'descuento':float(descuento),
                    'canal':"yambalu",
                    'consola':consola

                    })
        next=""
        enlaces = soup.find_all("a",class_="page-link")
        for enlace in enlaces:
            if str(enlace.string) == "»":
                page=page+1
                next=url+str(page)
                break
    return ofertas
