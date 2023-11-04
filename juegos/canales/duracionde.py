import requests
import json

def tratatiempo(tiempo):
    dev=0
    if tiempo is not None:
        dev=int(tiempo/60)
    return dev

def search(title=""):
    url = "https://duracionde.com/json/juegos?page=1&per_page=18&order_by=gameplay_count&name="+title

    payload={}
    headers = {
    'X-Requested-With': 'XMLHttpRequest'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    caracteristicas={}
    caracteristicas['lista'] = []
    respuesta=json.loads(response.text)
    for juego in respuesta["data"]:
        tiempos={}
        tiempos['tiempos'] = []
        tiempos['tiempos'].append({
            'clave': "main",
            'valor': tratatiempo(juego['stats']['modes']['main']['time'])
        })
        tiempos['tiempos'].append({
            'clave': "extras",
            'valor': tratatiempo(juego['stats']['modes']['extras']['time'])
        })
        tiempos['tiempos'].append({
            'clave': "complete",
            'valor': tratatiempo(juego['stats']['modes']['complete']['time'])
        })
        thumb=""
        if juego['cover']:
            thumb="https://duracionde.com/storage/images/"+juego['cover']
        caracteristicas['lista'].append({
            'titulo': juego['name'],
            'thumb':thumb,
            'id': juego['slug'],
            'detail':"https://duracionde.com/"+juego['slug'],
            'tiempos':tiempos['tiempos']
          })
    return caracteristicas

def detail(id):
    
    return json.loads({})


def ofertas(consola=""):
    return {}
