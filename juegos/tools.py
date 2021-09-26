from juegos.models import Juego,Oferta  # Import the model classes we just wrote.
import json
import juegos.canales.nintendo as n
import juegos.canales.sony as s
import juegos.canales.hl2b as HLTB
import juegos.canales.cex as cex
import juegos.canales.basecom as basecom
import juegos.canales.yambalu as yambalu
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
            logger.debug(transaction["title"])
            try:
                jbbdd = Juego.objects.get(idexterno=transaction["transaction_id"],tipo="d")
            except (KeyError, Juego.DoesNotExist):
                logger.warn("No existe "+transaction["title"])
                j = Juego(idexterno=transaction["transaction_id"],title=transaction["title"], tipo="d",consola="nsw")
                j.save()
                toolbuscajuegoswitch(j)
            except (KeyError, Juego.MultipleObjectsReturned):
                logger.error("existen varios "+transaction["title"])
            else:
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
            logger.debug(transaction["name"])
            try:
                jbbdd = Juego.objects.get(idexterno=transaction['entitlementId'],tipo='d')
            except (KeyError, Juego.DoesNotExist):
                logger.warn("No existe "+transaction["name"])
                j = Juego(idexterno=transaction["entitlementId"],title=transaction["name"], tipo="d",consola=transaction["platform"].lower(),image=transaction["image"]["url"])
                j.save()
            except (KeyError, Juego.MultipleObjectsReturned):
                logger.error("existen varios "+transaction["name"])
            else:
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
            logger.error("Error procesando "+juego.title)


def toolbuscajuegoswitch(juego):
    respuesta=n.search(juego.title)
    #print(juego.title)
    #search = json.loads(respuesta)
    if(len(respuesta["lista"])!=0):
        detalle=n.detail(respuesta["lista"][0]["detail"])
        juego.image=respuesta["lista"][0]["thumb"]
        juego.tamano=detalle["tamano"]
        juego.save()

def tooldetactualiza(juego_id,url,plataforma):
    if plataforma == 'nsw':
        detalle=n.detail(url)
        jbbdd = Juego.objects.get(id=juego_id)
        jbbdd.tamano=detalle["tamano"]
        jbbdd.image=detalle["thumb"]
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
            logger.error("Error procesando "+juego.title)


def toolofertas(canal=""):
    logger.info("Inicio toolofertas ->"+canal)
    Oferta.objects.all().delete()
    if canal=="basecom" or canal=="":
        logger.info("Inicio basecom")
        ofertas=basecom.ofertas("")
        for oferta in ofertas["lista"]:
            try:
                jbbdd = Oferta.objects.get(title=oferta["titulo"],consola=oferta["consola"])
                jbbdd.pBase=oferta["precio"]
                jbbdd.dBase=oferta["descuento"]
                jbbdd.detBase=oferta["detail"]
                jbbdd.save()                
            except (KeyError, Oferta.DoesNotExist):
                o = Oferta(title=oferta["titulo"],image=oferta["thumb"], pBase=oferta["precio"],dBase=oferta["descuento"],consola=oferta["consola"],detBase=oferta["detail"])
                o.save()
            except (KeyError, Oferta.MultipleObjectsReturned):
                logger.error("existen varios "+oferta["titulo"]+"("+oferta["consola"]+")")
            else:
                continue
        logger.info("Fin basecom")
    if canal=="yambalu" or canal=="":
        logger.info("Inicio yambalu")
        # Oferta.objects.filter(canal=1).delete()
        ofertas=yambalu.ofertas("")
        for oferta in ofertas["lista"]:
            try:
                jbbdd = Oferta.objects.get(title__contains=oferta["titulo"],consola=oferta["consola"])
                jbbdd.pYambalu=oferta["precio"]
                jbbdd.dYambalu=oferta["descuento"]
                jbbdd.detYambalu=oferta["detail"]
                jbbdd.save()                
            except (KeyError, Oferta.DoesNotExist):
                o = Oferta(title=oferta["titulo"],image=oferta["thumb"], pYambalu=oferta["precio"],consola=oferta["consola"],detYambalu=oferta["detail"],dYambalu=oferta["descuento"])
                o.save()
            except (KeyError, Oferta.MultipleObjectsReturned):
                logger.error("existen varios "+oferta["titulo"]+"("+oferta["consola"]+")")
            else:
                continue
        logger.info("Fin yambalu")

    logger.info("Fin toolofertas")