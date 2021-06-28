from juegos.models import Juego  # Import the model classes we just wrote.
import json
import juegos.canales.nintendo as n
import juegos.canales.sony as s
import juegos.canales.hl2b as HLTB
import juegos.canales.cex as cex
import sys
import logging

logger = logging.getLogger(__name__)

def toolcargaswitch(cookieSwitch=""):
    paso=100
    pagekey=0
    total=sys.maxsize
    while pagekey <= total:
        respuesta=n.transactions(limit=paso,offset=pagekey,cookie=cookieSwitch)
        trans = json.loads(respuesta)
        total=trans["total"]
        pagekey+=paso
        #print(trans["transactions"]) 
        for transaction in trans["transactions"]:
            #print(transaction["title"])
            try:
                jbbdd = Juego.objects.get(idexterno=transaction["transaction_id"])
            except (KeyError, Juego.DoesNotExist):
                # Redisplay the question voting form.
                j = Juego(idexterno=transaction["transaction_id"],title=transaction["title"], tipo="d",consola="nsw")
                j.save()
                toolbuscajuegoswitch(j)
            else:
                print("existe",transaction["title"])
                continue

def toolcargaps4(cookieps4=""):
    paso=100
    pagekey=0
    total=sys.maxsize
    while pagekey <= total:
        respuesta=s.transactions(limit=paso,offset=pagekey,cookie=cookieps4)
        trans = json.loads(respuesta)
        #print(trans["data"]["purchasedTitlesRetrieve"]["pageInfo"]["totalCount"])
        total=trans["data"]["purchasedTitlesRetrieve"]["pageInfo"]["totalCount"]
        pagekey+=paso
        for transaction in trans["data"]["purchasedTitlesRetrieve"]["games"]:
            #print(transaction["title"])
            try:
                jbbdd = Juego.objects.get(idexterno=transaction['entitlementId'])
            # except (KeyError, Juego.DoesNotExist):
            except:
                # Redisplay the question voting form.
                j = Juego(idexterno=transaction["entitlementId"],title=transaction["name"], tipo="d",consola="ps4",image=transaction["image"]["url"])
                j.save()
            else:
                print("existe",transaction["name"])
                continue

def toolactualizajuegos():
    lista=Juego.objects.all()
    for juego in lista:
        try:
            if juego.title != "" and juego.title != None:
                if juego.visible == True and juego.terminado == False:
                    if juego.consola == 'nsw':
                        if juego.tamano == 0:
                            toolbuscajuegoswitch(juego)
                    if juego.tiempo == 0:
                        respuesta=HLTB.search(juego.title)
                        if len(respuesta["lista"])>0 and len(respuesta["lista"][0]["tiempos"])>0:
                            juego.tiempo=respuesta["lista"][0]["tiempos"][0]["valor"]
                            juego.save()
                if juego.venta == True:
                    if juego.idPrecio != "" or juego.idPrecio != None: 
                        respuesta=cex.search(juego.title)
                        if respuesta["response"]["data"]["totalRecords"]>0:
                            juego.idPrecio=respuesta["response"]["data"]["boxes"][0]["boxId"]
                            juego.save()
                    respuesta=cex.detail(juego.idPrecio)
                    juego.precio=respuesta["response"]["data"]["boxDetails"][0]["sellPrice"]
                    juego.save()
        except: 
            print("Error procesando "+juego.title)


def toolbuscajuegoswitch(juego):
    respuesta=n.search(juego.title)
    #print(juego.title)
    #search = json.loads(respuesta)
    if(len(respuesta["lista"])!=0):
        sdetalle=n.detail(respuesta["lista"][0]["detail"])
        detalle = json.loads(sdetalle)
        juego.image=respuesta["lista"][0]["thumb"]
        juego.tamano=detalle["tamano"]
        juego.save()

def tooldetactualiza(juego_id,url,plataforma):
    if plataforma == 'nsw':
        respuesta=n.detail(url)
        detalle = json.loads(respuesta)
        jbbdd = Juego.objects.get(id=juego_id)
        jbbdd.tamano=detalle["tamano"]
        jbbdd.image=detalle["imagen"]
        jbbdd.save()
    elif plataforma == 'ps4':
        cadena="0"
    else:
        cadena="0"

def tooldetactualizatiempo(juego_id,url):
    respuesta=HLTB.detail(url)
    jbbdd = Juego.objects.get(id=juego_id)
    jbbdd.tiempo=respuesta["lista"][0]["tiempos"][0]["valor"]
    jbbdd.save()

def toolpreciojuegos():
    lista=Juego.objects.all()
    for juego in lista:
        try:
            if juego.venta == True:
                if juego.idPrecio == "" or juego.idPrecio == None: 
                    respuesta=cex.search(juego.title)
                    if respuesta["response"]["data"]["totalRecords"]>0:
                        juego.idPrecio=respuesta["response"]["data"]["boxes"][0]["boxId"]
                        juego.save()
                respuesta=cex.detail(juego.idPrecio)
                juego.precio=respuesta["response"]["data"]["boxDetails"][0]["sellPrice"]
                juego.save()
        except:
            print("Error procesando "+juego.title)