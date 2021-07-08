import requests
import json

def transactions(limit=100,offset=0,cookie=""):
    url = "https://web.np.playstation.com/api/graphql/v1/op?operationName=getPurchasedGameList&variables={\"isActive\":true,\"platform\":[\"ps4\",\"ps5\"],\"size\":"+str(limit)+",\"start\":"+str(offset)+",\"sortBy\":\"ACTIVE_DATE\",\"sortDirection\":\"desc\",\"subscriptionService\":\"NONE\"}&extensions={\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"2c045408b0a4d0264bb5a3edfed4efd49fb4749cf8d216be9043768adff905e2\"}}"
    payload={}
    headers = {
    'Host': 'web.np.playstation.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Accept': 'application/json',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://library.playstation.com/recently-purchased',
    'content-type': 'application/json',
    'X-PSN-App-Ver': 'my-playstation/0.1.0-20201117173737-hotfix-2-g86cc0018-86cc0018643ea03b97fd5bf4b534df2c7a80b99f',
    'X-PSN-Correlation-Id': 'd9c6c550-7fc2-498d-9350-616234e773d5',
    'X-PSN-Request-Id': 'c22277aa-3281-4740-9b11-d1a865a44723',
    'Origin': 'https://library.playstation.com',
    'Connection': 'keep-alive',
    'Cookie': cookie
    }    

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text

def search(title):
    url = "https://web.np.playstation.com/api/graphql/v1//op?operationName=getSearchResults&variables={\"countryCode\":\"ES\",\"languageCode\":\"es\",\"nextCursor\":\"CBgaTgokM2I3MjNmMWM4MzNmNDk5M2E0ZmU2NWE0MjczNDkzOTQtOTMyEiZzZWFyY2gtcmVsZXZhbmN5LWNvbmNlcHQtZ2FtZS1hbGwtdG9wayIec2VhcmNoLm5vX2V4cGVyaW1lbnQubm9uLjAubm9uKgM3ODU\",\"pageOffset\":0,\"pageSize\":24,\"searchTerm\":\""+title+"\"}&extensions={\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"886102a3a6c2d2d80d5702fbe8fbf960e535bf85dfa7f5d5bf67dcc2775be177\"}}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    sresponse=json.loads(response.text)
    respuesta={}
    respuesta['lista'] = []
    for juego in sresponse["data"]["universalSearch"]["results"]:
        thumb=""
        for media in juego["media"]:
            if media["role"] == "MASTER":
                thumb=media["url"]
        consola="ps4"
        if len(juego["platforms"]) >0:
            consola=juego["platforms"][0].lower()
        respuesta['lista'].append({
            'titulo': juego["name"],
            'thumb':thumb,
            'id': juego["id"],
            'detail':"https://store.playstation.com/es-es/product/"+juego["id"],
            'consola':consola
            })

    return respuesta

    
