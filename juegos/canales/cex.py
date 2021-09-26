import requests
import json

def search(title="",categoria=""):
    caracteristicas={}
    caracteristicas['lista'] = []
    cat=""
    if categoria == "nsw":
        cat="&categoryIds=[1031]"
    elif categoria == "ps4":
        cat="&categoryIds=[1001]"
    url = "https://wss2.cex.es.webuy.io/v3/boxes?q="+title+cat+"&firstRecord=1&count=50&sortBy=popularity&sortOrder=desc"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    listajuegos=json.loads(response.text)
    # return json.loads(response.text)
    for juego in listajuegos["response"]["data"]["boxes"]:
        precios={}
        precios['precios'] = []
        precios['precios'].append({
            'clave': "Vendemos",
            'valor': juego["sellPrice"]
        })
        precios['precios'].append({
            'clave': "Compramos",
            'valor': juego["cashPrice"]
        })
        precios['precios'].append({
            'clave': "Intercambiamos",
            'valor': juego["exchangePrice"]
        })

        caracteristicas['lista'].append({
            'titulo': juego["boxName"],
            'thumb':juego["imageUrls"]["small"],
            'id': juego["boxId"],
            'detail':"https://wss2.cex.es.webuy.io/v3/boxes/"+juego["boxId"]+"/detail",
            'precios':precios['precios']
          })
    return caracteristicas

def detail(id):
    
    url = "https://wss2.cex.es.webuy.io/v3/boxes/"+id+"/detail"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)

def ofertas(consola=""):
    return {}
