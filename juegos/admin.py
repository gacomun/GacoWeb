from django.contrib import admin

from .models import Juego

@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ('title','tipo', 'consola')
    list_filter = ('tipo', 'consola','terminado','visible')
    search_fields = ['title','tamano',"idexterno"]