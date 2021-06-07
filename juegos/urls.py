from django.urls import path

from . import views

app_name = 'juegos'
urlpatterns = [
    # ex: /juegos/
    path('', views.index, name='index'),
    # ex: /juegos/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /juegos/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /juegos/tools/
    path('tools/', views.tools, name='tools'),
    # ex: /juegos/tools/cargaswitch
    path('tools/carga', views.carga, name='carga'),
    # ex: /juegos/tools/actualiza
    path('tools/actualiza', views.actualiza, name='actualiza'),
    # ex: /juegos/tools/actualiza
    path('tools/precios', views.precios, name='precios'),
    # ex: /juegos/5/actualiza
    path('<int:juego_id>/actualiza', views.detactualiza, name='detactualiza'),
    # ex: /juegos/5/actualiza
    path('<int:juego_id>/actualizatiempo', views.detactualizatiempo, name='detactualizatiempo'),
    # ex: /juegos/5/nintendo/
    path('tools/carga', views.carga, name='carga'),
]
