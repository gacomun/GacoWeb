import requests
from bs4 import BeautifulSoup


def tratatamano(cadena):
    cadena = cadena.replace("MB", "")
    cadena = cadena.replace(",", ".")
    return cadena


def transactions(limit=100,offset=0,cookie=""):
    url = "https://ec.nintendo.com/api/my/transactions?limit="+ str(limit) +"&offset="+str(offset)

    payload={}
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://ec.nintendo.com/my/',
    'Cookie': cookie
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text

def searchgame(title=""):
    url = "https://searching.nintendo-europe.com/es/select?q="+title+"&fq=type:GAME AND sorting_title:* AND *:*&sort=score desc, date_from desc&start=0&rows=24&wt=json&bf=linear(ms(priority,NOW/HOUR),1.1e-11,0)&bq=!deprioritise_b:true^999"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text

def detail(title=""):
    tamano=0
    r = requests.get(title)
    soup = BeautifulSoup(r.text, 'lxml')
    if len(soup.find_all('div',class_="listwheader-container")) != 0 :
        listat = soup.find_all('div',class_="listwheader-container")#[0].find_all('div')
    elif len(soup.find_all('div',class_="row game_info_container game-details-container info_system")) != 0 :
        listat = soup.find_all('div',class_="row game_info_container game-details-container info_system")#[0].find_all('div')
    else:
        listat={}
    for enlat in listat:
        lista=enlat.find_all('div')
        for enlace in lista:
            listap=enlace.find_all("p")
            if listap:
        #    if("Tamaño de la descarga" not in listap[0].string)
                if "de la descarga" in listap[0].string:
                        tamano= float(tratatamano(listap[1].string))
    imagen = soup.find_all('vc-price-box-standard')[0][":packshot-src"]
    data = "{\"tamano\": "+str(tamano)+",\"imagen\":\"https:"+imagen.replace("'", "")+"\"}"
    return(data)