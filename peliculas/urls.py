from django.urls import path

from . import views

app_name = 'peliculas'
urlpatterns = [
    # ex: /peliculas/
    path('', views.index, name='index'),

]
