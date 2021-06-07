import requests

import juegos.canales.cex as cex

respuesta=cex.search("beyond","ps4")
print(respuesta)

respuesta=cex.search("beyond","nsw")
print(respuesta)

respuesta=cex.detail("8436566141673")
print(respuesta)
