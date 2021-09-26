from django.contrib import admin

from .models import Juego,Oferta,Property

@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ('title','tipo', 'consola')
    list_filter = ('tipo', 'consola','terminado','visible')
    search_fields = ['title','tamano',"idexterno"]

@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ('title','consola')
    list_filter = ['consola']
    search_fields = ['title']

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('clave','valor')
    search_fields = ['clave','valor']