from django.contrib import admin

from .models import Pelicula,Canal

@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']
    search_fields = ['title']

@admin.register(Canal)
class CanalAdmin(admin.ModelAdmin):
    # list_display = ()
    # list_filter = []
    search_fields = []
