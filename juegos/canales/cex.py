import requests
import json

def search(title="",categoria=""):
    cat=""
    if categoria == "nsw":
        cat="&categoryIds=[1031]"
    elif categoria == "ps4":
        cat="&categoryIds=[1001]"
    url = "https://wss2.cex.es.webuy.io/v3/boxes?q="+title+cat+"&firstRecord=1&count=50&sortBy=popularity&sortOrder=desc"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)

def detail(id):
    
    url = "https://wss2.cex.es.webuy.io/v3/boxes/"+id+"/detail"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)
