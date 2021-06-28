from bs4 import BeautifulSoup
import http.client
import requests
import sys

def limpiatexto(cadena):
  cadena = cadena.replace("\t", "")
  cadena = cadena.replace("\n", "")
  cadena = cadena.replace("™", "")
  cadena = cadena.replace("®", "")
  return cadena

def tratatiempo(cadena):
  try:
    cadena = limpiatexto(cadena)
    if "½" in cadena:
      cadena = cadena.replace("½", ".5")
    if "Hours" in cadena:
      cadena = cadena.replace("Hours", "")
      cadena = cadena.replace(" ", "")
      cadena = cadena.split(sep="-")[0]
      temp=float(cadena)*60
      cadena=str(temp)
    elif "Mins" in cadena:
      cadena = cadena.replace("Mins", "")
      cadena = cadena.replace(" ", "")
      cadena = cadena.split(sep="-")[0]
    elif "--" in cadena:
      cadena="0"
    else:
      print("No coincide "+ cadena)
  except:
    cadena="0"

  return cadena


def search(title=""):
    caracteristicas={}

    conn = http.client.HTTPSConnection("howlongtobeat.com")
    payload = 'queryString='+limpiatexto(title)+'&t=games&sorthead=popular&sortd=Normal%20Order&plat=&length_type=main&length_min=&length_max=&v=&f=&g=&detail=&randomize=0'
    headers = {
    'Host': 'howlongtobeat.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Accept': '*/*',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Content-type': 'application/x-www-form-urlencoded',
    'Origin': 'https://howlongtobeat.com',
    'Referer': 'https://howlongtobeat.com/'
    }
    conn.request("POST", "/search_results?page=1", payload, headers)
    res = conn.getresponse()
    data = res.read()
    # print(data.decode("utf-8"))
    soup = BeautifulSoup(data.decode("utf-8"), 'lxml')
    listajuegos=soup.find_all("li")
    caracteristicas['lista'] = []
    for juego in listajuegos:
        try:
          nombre=juego.find_all('h3',class_="shadow_text")[0].find_all("a")[0].string
          datos=juego.find_all('div',class_="search_list_tidbit")
          par=False
          tiempos={}
          tiempos['tiempos'] = []
          id=juego.find_all('a')[0].attrs['href'].replace("game?id=","")
          thumb="https://howlongtobeat.com"+juego.find_all('img')[0].attrs['src']
          detail="https://howlongtobeat.com/"+juego.find_all('a')[0].attrs['href']
          for dato in datos:
              if par ==False:
                  clave=dato.string
                  par=True
              else:
                  tiempos['tiempos'].append({
                      'clave': clave,
                      'valor': float(tratatiempo(dato.string))
                  })
                  par=False
          caracteristicas['lista'].append({
            'titulo': limpiatexto(nombre),
            'thumb':thumb,
            'id': id,
            'detail':detail,
            'tiempos':tiempos['tiempos']
          })
        except:
          print("hl2b -> search: Error procesando "+title)
    return caracteristicas

def detail(url=""):
  caracteristicas={}
  caracteristicas['lista'] = []
  conn = http.client.HTTPSConnection("howlongtobeat.com")
  headers = {
  'Host': 'howlongtobeat.com',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
  'Accept': '*/*',
  'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
  'Content-type': 'application/x-www-form-urlencoded',
  'Origin': 'https://howlongtobeat.com',
  'Referer': 'https://howlongtobeat.com/'
  }
  payload = ''
  conn.request("GET", url, payload, headers)
  res = conn.getresponse()
  data = res.read()
  soup = BeautifulSoup(data, 'lxml')
  lista = soup.find_all('div',class_="game_times")[0].find_all('li')
  nombre= soup.find_all('div',class_="profile_header shadow_text")[0].string
  par=False
  tiempos={}
  tiempos['tiempos'] = []
  for dato in lista:
    clave=dato.find_all('h5')[0].string
    valor=float(tratatiempo(dato.find_all('div')[0].string))
    tiempos['tiempos'].append({
        'clave': clave,
        'valor': valor
    })
  caracteristicas['lista'].append({
  'titulo': limpiatexto(nombre),
  'tiempos':tiempos['tiempos']
  })
      # print(dato.string)
  return caracteristicas
