import requests
import json
from ..models import Property 

def limpiatexto(cadena):
  cadena = cadena.replace("\t", "")
  cadena = cadena.replace("\n", "")
  cadena = cadena.replace("™", "")
  cadena = cadena.replace("®", "")
  cadena = cadena.replace("£", "")
  return cadena


def getexchangerate(origen, destino):
    apikey=Property.objects.all().filter(clave="exchangerate-api.apikey")
    url = "https://v6.exchangerate-api.com/v6/"+apikey.valor+"/pair/"+origen+"/"+destino

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    
    sresponse=json.loads(response.text)

    return float(sresponse["conversion_rate"])