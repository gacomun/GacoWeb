import logging
from bs4 import BeautifulSoup
import requests
import juegos.canales.tools as tools

# Create a logger for this file
logger = logging.getLogger(__file__)
cambio=1.1767
#cambio=tools.getexchangerate("GBP","EUR")

def tratar_title(cadena):
    cadena=cadena.replace("(PS5)","")
    cadena=cadena.replace("(Nintendo Switch)","")
    cadena=cadena.replace("(PS4)","")
    cadena=cadena.replace("[Code in a Box]","")
    cadena=cadena.replace("(Download Code in Box)","")
    cadena=cadena.replace("(Code In Box)","")
    cadena=cadena.rstrip()
    return cadena

def search(title=""):
    return {}

def detail(title=""):
    return {}

def ofertas(consola=""):
    ofertas={}
    ofertas['lista'] = []
    if consola=="nsw" or consola=="":
        next="https://www.base.com/games/switch/pg735/bn10008264/products.htm"
        filtro="?filter=a%3a523%3a375630"        
        ofertas=trataPagina(next,filtro,"nsw",ofertas)
    if consola=="ps4" or consola=="":
        next="https://www.base.com/games/playstation/bestseller/pg735/bn10009009/games.htm"
        filtro="?filter=a%3a568%3a385582"
        ofertas=trataPagina(next,filtro,"ps4",ofertas)
    if consola=="ps5" or consola=="":
        next="https://www.base.com/games/playstation/bestseller/pg735/bn10009009/games.htm"
        filtro="?filter=a%3a568%3a385583"
        ofertas=trataPagina(next,filtro,"ps5",ofertas)
        
    return ofertas

def trataPagina(url,filtro,consola,ofertas):
    next =url+filtro
    while next != "":
        r = requests.get(next)
        soup = BeautifulSoup(r.text, 'lxml')
        grupos = soup.find_all('div',class_="product-list")
        for grupo in grupos:
            juegos = grupo.find_all('li')
            for juego in juegos:
                titulo=tools.limpiatexto(juego.find('div',class_="title").string)
                thumb=juego.find('img').attrs['src']
                if juego.find('span',class_="price").find('a') is not None :
                    detail=juego.find('span',class_="price").find('a').attrs['href']
                    precio=float(tools.limpiatexto(juego.find('span',class_="price").find('a').string))
                    precio=precio*cambio
                    descprecio=0
                    if juego.find('span',class_="yousave") is not None:
                        descprecio=float(tools.limpiatexto(juego.find('span',class_="yousave").find('em').string))
                        descprecio=descprecio*cambio
                    total=precio+descprecio
                    descuento=(descprecio*100)/total
                    ofertas['lista'].append({
                        'titulo': tratar_title(titulo),
                        'thumb':"https://www.base.com"+thumb,
                        'detail': "https://www.base.com"+detail,
                        'precio':precio,
                        'descuento':descuento,
                        'total':total,
                        'canal':"basecom",
                        'consola':consola
                    })
        next=""
        enlaces = soup.find_all("a")
        for enlace in enlaces:
            if str(enlace.string) == "Next":
                next=url+enlace.attrs['href']
    return ofertas
