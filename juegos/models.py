from django.db import models


class Juego(models.Model):
    id = models.IntegerField
    idexterno = models.CharField(max_length=200,null=True)
    title = models.CharField(max_length=200,null=True)
    image = models.CharField(max_length=200, null=True, default='', blank=True)
    tamano = models.IntegerField(default=0)
    ENUM_TIPO = (
        ('d', 'Digital'),
        ('f', 'Fisico'),
    )
    tipo = models.CharField(
        max_length=1,
        choices=ENUM_TIPO,
        blank=True,
        default='d')
    ENUM_CONSOLA = (
        ('nsw', 'SWITCH'),
        ('ps4', 'PS4'),
    )
    consola = models.CharField(
        max_length=3,
        choices=ENUM_CONSOLA,
        blank=True)
    tiempo = models.IntegerField(default=0)
    terminado = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    venta = models.BooleanField(default=False)
    precio = models.FloatField(default=0.0) 
    idPrecio = models.CharField(max_length=200,null=True, default='', blank=True)
    
    def __str__(self):
        return self.title    

    def getratio(self):
        if self.tiempo == 0:
            return 0.00
        else:
            return float("{:.2f}".format(self.tamano/self.tiempo))    
    def getconsola(self):
        if self.consola == "nsw":
            return "Switch"
        if self.consola == "ps4":
            return "PS4"
        else:
            return "Sin texto"

    def gettiempohora(self):
        return float("{:.2f}".format(self.tiempo/60))    

    def gettipo(self):
        if self.tipo == "d":
            return "Digital"
        if self.tipo == "f":
            return "Fisico"
        else:
            return "Sin texto"
