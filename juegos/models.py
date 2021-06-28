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
        ('ps5', 'PS5'),
        ('3ds', '3DS'),
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
    ENUM_ESTADO = (
        ('n', 'Nuevo'),
        ('u', 'Usado')
    )
    estado = models.CharField(
        max_length=1,
        choices=ENUM_ESTADO,
        blank=True,
        default='u')
    
    def __str__(self):
        return (self.title, "")[self.title is None]    

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
        if self.consola == "ps5":
            return "PS5"
        if self.consola == "3ds":
            return "3DS"
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

    def getestado(self):
        if self.estado == "u":
            return "Usado"
        if self.estado == "n":
            return "Nuevo"
        else:
            return "Sin texto"

    def toJson(self):
        idprecio=""
        if(self.idPrecio is not None):
            idprecio=self.idPrecio
        return ({
                'id': self.id,
                'idexterno': self.idexterno,
                'title': self.title,
                'image': self.image,
                'tamano': self.tamano,
                'tipo': {
                    'id':self.tipo,
                    'descripcion':self.gettipo()
                    },
                'consola': {
                    'id':self.consola,
                    'descripcion':self.getconsola()
                    },
                'tiempo':self.gettiempohora(),
                'terminado':self.terminado,
                'visible':self.visible,
                'venta':self.venta,
                'precio':self.precio,
                'idPrecio':idprecio,
                'estado': {
                    'id':self.estado,
                    'descripcion':self.getestado()
                    },
                'ratio':self.getratio()

                })