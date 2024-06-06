from django.db import models

class Canal(models.Model):
    pass
class Pelicula(models.Model):
    id = models.IntegerField
    title = models.CharField(max_length=200,null=True)
    poster_path = models.CharField(max_length=200,null=True)
    canales = models.ManyToManyField(Canal)