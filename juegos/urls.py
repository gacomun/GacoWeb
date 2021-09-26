from django.urls import path

from . import views
from . import juegosrest as rest

app_name = 'juegos'
urlpatterns = [
    # ex: /juegos/
    path('', views.index, name='index'),
    # ex: /juegos/5/
    path('<int:pk>/', views.detail, name='detail'),
    # ex: /juegos/tools/
    path('tools/', views.tools, name='tools'),
    # ex: /juegos/5/actualiza
    # path('<int:juego_id>/actualiza', views.detactualiza, name='detactualiza'),
    # ex: /juegos/5/actualiza
    # path('<int:juego_id>/actualizatiempo', views.detactualizatiempo, name='detactualizatiempo'),
    # ex: /juegos/tools/searchjuego
    # path('tools/searchjuego', views.searchjuego, name='searchjuego'),
    # ex: /juegos/tools/searchjuego
    # path('<int:juego_id>/searchjuego', views.detsearchjuego, name='detsearchjuego'),
    # ex: /juegos/canales/search
    path('canales/search', views.canalsearch, name='canalsearch'),
    # ex: /juegos/ofertas
    path('ofertas/', views.ofertasindex, name='ofertasindex'),


    # REST
    # ex: GET POST /juegos/rest/v0/juegos/
    path('rest/v0/juegos/', rest.juego_list),
    # ex: PUT PATCH DELETE /juegos/rest/v0/juegos/1
    path('rest/v0/juegos/<int:pk>', rest.juego_detail),
    # ex: PUT PATCH DELETE /juegos/rest/v0/juegos/1
    path('rest/v0/juegos/<int:pk>/actualiza', rest.juego_detail_actualiza),
    # ex: GET/juegos/rest/v0/juegos/
    path('rest/v0/canales/<str:canal>', rest.canal_detail),
    # ex: GET/juegos/rest/v0/tools/carga
    path('rest/v0/tools/carga', rest.tools_carga_list),
    # ex: /juegos/rest/v0/tools/actualiza
    path('rest/v0/tools/actualiza', rest.tools_actualiza_list),
    # ex: /juegos/rest/v0/tools/tools/precios
    path('rest/v0/tools/precios', rest.tools_precios_list),
    # ex: /juegos/rest/v0/tools/tools/duplicados
    #path('rest/v0/tools/duplicados', rest.tools_duplicados_list),
    # ex: /juegos/rest/v0/ofertas
    path('rest/v0/ofertas/', rest.ofertas_list),
    # ex: /juegos/rest/v0/tools/ofertas
    path('rest/v0/tools/ofertas', rest.tools_ofertas_list),


]
