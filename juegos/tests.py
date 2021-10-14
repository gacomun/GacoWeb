from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .models import Juego,Oferta

class JuegoModelTests(TestCase):

    def test_getratio(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        juego = Juego(tiempo=0,tamano=0)
        self.assertEqual(juego.getratio(), 0.0)
        juego = Juego(tiempo=0,tamano=1)
        self.assertEqual(juego.getratio(), 0.0)
        juego = Juego(tiempo=0,tamano=-1)
        self.assertEqual(juego.getratio(), 0.0)
        juego = Juego(tiempo=1,tamano=0)
        self.assertEqual(juego.getratio(), 0.0)
        juego = Juego(tiempo=-1,tamano=0)
        self.assertEqual(juego.getratio(), 0.0)
        juego = Juego(tiempo=1,tamano=1)
        self.assertEqual(juego.getratio(), 1.0)
        juego = Juego(tiempo=1,tamano=-1)
        self.assertEqual(juego.getratio(), -1.0)
        juego = Juego(tiempo=-1,tamano=-1)
        self.assertEqual(juego.getratio(), 1.0)
        juego = Juego(tiempo=-1,tamano=1)
        self.assertEqual(juego.getratio(), -1.0)

    def test_getstr(self):
        juego = Juego(title="The room")
        self.assertEqual(juego.__str__(),"The room")

    def test_getconsola(self):
        juego = Juego(consola="nsw")
        self.assertEqual(juego.getconsola(),"Switch")
        juego.consola="ps4"
        self.assertEqual(juego.getconsola(),"PS4")
        juego.consola="ps5"
        self.assertEqual(juego.getconsola(),"PS5")
        juego.consola="3ds"
        self.assertEqual(juego.getconsola(),"3DS")
        juego= Juego()
        self.assertEqual(juego.getconsola(),"Sin texto")
        juego= Juego(consola="")
        self.assertEqual(juego.getconsola(),"Sin texto")
        juego= Juego(consola="abc")
        self.assertEqual(juego.getconsola(),"Sin texto")

    def test_gettiempohora(self):
        juego = Juego(tiempo=60)
        self.assertEqual(juego.gettiempohora(),1.0)

    def test_gettipo(self):
        juego= Juego(tipo="d")
        self.assertEqual(juego.gettipo(),"Digital")
        juego.tipo="f"
        self.assertEqual(juego.gettipo(),"Fisico")
        juego.tipo="a"
        self.assertEqual(juego.gettipo(),"Sin texto")
        
    def test_getestado(self):
        juego= Juego(estado="u")
        self.assertEqual(juego.getestado(),"Usado")
        juego.estado="n"
        self.assertEqual(juego.getestado(),"Nuevo")
        juego.estado="a"
        self.assertEqual(juego.getestado(),"Sin texto")
    def test_toJson(self):
        juego= Juego(estado="u")
        # self.assertEqual(juego.toJson(),"Usado")
    def test_isValidConsola(self):
        juego= Juego(consola="nsw")
        self.assertTrue(juego.isValidConsola())
        juego= Juego(consola="ps4")
        self.assertTrue(juego.isValidConsola())
        juego= Juego(consola="ps5")
        self.assertTrue(juego.isValidConsola())
        juego= Juego(consola="3ds")
        self.assertTrue(juego.isValidConsola())
        juego= Juego()
        self.assertFalse(juego.isValidConsola())
        juego= Juego(consola="")
        self.assertFalse(juego.isValidConsola())
        juego= Juego(consola="abc")
        self.assertFalse(juego.isValidConsola())
    def test_getPorcentaje(self):
        juego= Juego(estado="u")
        self.assertEqual(juego.getPorcentaje(juego),100)


def create_juego(title):
    
    return Juego.objects.create(title=title)


class JuegoIndexViewTests(TestCase):
    def test_no_juegos(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('juegos:index'))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "No juegos are available.")
        # self.assertQuerysetEqual(response.context['juego_list'], [])

    # def test_two_juegos(self):
    #     juego1 = create_juego(title="Past question 1.")
    #     juego2 = create_juego(title="Past question 2.")
    #     response = self.client.get(reverse('juegos:index'))
    #     self.assertQuerysetEqual(
    #         response.context['juego_list'],
    #         [juego1, juego2],
    #     )

import juegos.canales.nintendo as n
import json
class CanalNintendoTests(TestCase):

    def test_tratatamano(self):
        cadena=n.tratatamano("")
        self.assertEqual(cadena,"")
        cadena=n.tratatamano("100 MB")
        self.assertEqual(cadena,"100 ")
        cadena=n.tratatamano("1000,00 MB")
        self.assertEqual(cadena,"1000.00 ")
        cadena=n.tratatamano("1000000,00 MB")
        self.assertEqual(cadena,"1000000.00 ")

    def test_trataConsola(self):
        cadena=n.trataConsola("")
        self.assertEqual(cadena,"N/A")
        cadena=n.trataConsola("Nintendo Switch")
        self.assertEqual(cadena,"nsw")
        cadena=n.trataConsola("3ds_downloadsoftware")
        self.assertEqual(cadena,"3ds")
        cadena=n.trataConsola("nintendoswitch_downloadsoftware")
        self.assertEqual(cadena,"nsw")
        cadena=n.trataConsola("dsi_dsiware,3ds_dsiware")
        self.assertEqual(cadena,"3ds")
        cadena=n.trataConsola("nds_cartridge")
        self.assertEqual(cadena,"nds")
        cadena=n.trataConsola("wii_disc,wiiu_wiidigitaldistribution")
        self.assertEqual(cadena,"wiiu")
        cadena=n.trataConsola("wii_disc")
        self.assertEqual(cadena,"wii")
        cadena=n.trataConsola("nds_cartridge,wiiu_virtualconsole")
        self.assertEqual(cadena,"nds")
        cadena=n.trataConsola("gameboyadvance_cartridge")
        self.assertEqual(cadena,"gba")
        
    
    def test_searchgame(self):
        cadena=n.search("overcooked")
        #lista = json.loads(cadena)
        self.assertNotEqual(len(cadena),0)
        cadena=n.search("breath of the wild")
        self.assertNotEqual(len(cadena),0)
        

    def test_detail(self):        
        sal=n.detail("https://www.nintendo.es/Juegos/Nintendo-Switch/Overcooked-2-1388792.html")
        self.assertTrue(sal)
        self.assertNotEqual(sal["tamano"],0)
        self.assertTrue(sal["title"],0)
        sal=n.detail("https://www.nintendo.es/Contenido-descargable/Overcooked-2-Surf-n-Turf-1454782.html")
        self.assertTrue(sal)
        self.assertNotEqual(sal["tamano"],0)
        self.assertTrue(sal["title"],0)
        sal=n.detail("https://www.nintendo.es/Juegos/Programas-descargables-Nintendo-Switch/Coffee-Crisis-1468498.html")
        self.assertTrue(sal)
        self.assertNotEqual(sal["tamano"],0)
        self.assertTrue(sal["title"],0)

import juegos.canales.sony as s
class CanalSonyTests(TestCase):

    def test_searchgame(self):
        cadena=s.search("horizon zero")
        self.assertNotEqual(len(cadena),0)
        cadena=s.search("control")
        self.assertNotEqual(len(cadena),0)

import juegos.canales.hl2b as HLTB
class Canalhl2bTests(TestCase):

    def test_tratatiempo(self):
        cadena=HLTB.tratatiempo("1½ Hours")
        self.assertEqual(cadena,"90.0")
        cadena=HLTB.tratatiempo("Hours")
        self.assertEqual(cadena,"0")
        cadena=HLTB.tratatiempo("Mins")
        self.assertEqual(cadena,"")
        cadena=HLTB.tratatiempo("--")
        self.assertEqual(cadena,"0")

    def test_search(self):
        salida=HLTB.search("The room")
        self.assertTrue(salida)
        salida=HLTB.search("legado")
        self.assertTrue(salida)

    def test_detail(self):
        salida=HLTB.detail("/game?id=65442")
        self.assertTrue(salida)

import juegos.tools as t
class ToolsTests(TestCase):

    def test_toolactualizajuegos(self):
        t.toolactualizajuegos()
        lista=Juego.objects.all()
        self.assertEqual(len(lista),0)

        juego = Juego(id=0,title="The room",consola="ps4")
        juego.save()
        t.toolactualizajuegos()
        jbbdd = Juego.objects.get(id=0)
        self.assertEqual(jbbdd.image,"")
        self.assertEqual(jbbdd.tamano,0)

        jbbdd.consola="nsw"
        jbbdd.save()
        t.toolactualizajuegos()
        jbbdd = Juego.objects.get(id=0)
        self.assertNotEqual(jbbdd.image,"")
        self.assertNotEqual(jbbdd.tamano,0)

        jbbdd.tiempo=0
        jbbdd.save()
        t.toolactualizajuegos()
        jbbdd = Juego.objects.get(id=0)
        self.assertNotEqual(jbbdd.tiempo,0)

        jbbdd.venta=True
        jbbdd.idPrecio="5030941116350"
        jbbdd.save()
        t.toolactualizajuegos()
        jbbdd = Juego.objects.get(id=0)
        self.assertEqual(jbbdd.precio,0.0)

    def test_toolbuscajuegoswitch(self):
        juego = Juego(id=1,title="jdasdhas",consola="nsw")
        juego.save()
        t.toolbuscajuegoswitch(juego)
        juego = Juego.objects.get(id=1)
        self.assertEqual(juego.image,"")
        self.assertEqual(juego.tamano,0)
        juego.title="Coffee Crisis"
        t.toolbuscajuegoswitch(juego)
        juego = Juego.objects.get(id=1)
        self.assertNotEqual(juego.image,"")
        self.assertNotEqual(juego.tamano,0)

    def test_tooldetactualiza(self):
        juego = Juego(id=2)
        juego.save()
        t.tooldetactualiza(2,"https://www.nintendo.es/Juegos/Programas-descargables-Nintendo-Switch/Coffee-Crisis-1468498.html","adf")
        juego = Juego.objects.get(id=2)
        self.assertEqual(juego.image,"")
        self.assertEqual(juego.tamano,0)
        t.tooldetactualiza(2,"https://www.nintendo.es/Juegos/Programas-descargables-Nintendo-Switch/Coffee-Crisis-1468498.html","ps4")
        juego = Juego.objects.get(id=2)
        self.assertEqual(juego.image,"")
        self.assertEqual(juego.tamano,0)
        t.tooldetactualiza(2,"https://www.nintendo.es/Juegos/Programas-descargables-Nintendo-Switch/Coffee-Crisis-1468498.html","nsw")
        juego = Juego.objects.get(id=2)
        self.assertNotEqual(juego.image,"")
        self.assertNotEqual(juego.tamano,0)
        t.tooldetactualiza(2,"https://www.nintendo.es//Juegos/Programas-descargables-Nintendo-Switch/Sky-Ninios-de-la-Luz-1742945.html","nsw")
        juego = Juego.objects.get(id=2)
        self.assertNotEqual(juego.image,"")
        self.assertNotEqual(juego.tamano,0)
        

    def test_tooldetactualizatiempo(self):
        juego = Juego(id=3)
        juego.save()
        t.tooldetactualizatiempo(3,"/game?id=65442")
        juego = Juego.objects.get(id=3)
        self.assertNotEqual(juego.tiempo,0)

    def test_toolpreciojuegos(self):
        juego = Juego(id=4)
        juego.venta=True
        juego.title="Control"
        juego.save()
        t.toolpreciojuegos()
    def test_toolofertas(self):
        t.toolofertas("")

import juegos.canales.cex as cex
class CanalcexTests(TestCase):

    def test_search(self):
        salida=cex.search("beyond","ps4")
        self.assertTrue(salida)
        salida=cex.search("beyond","nsw")
        self.assertTrue(salida)
    def test_detail(self):
        salida=cex.detail("8436566141673")
        self.assertTrue(salida)
        salida=cex.detail("711719878346")
        self.assertTrue(salida)

import juegos.canales.duracionde as duracionde
class CanalduraciondeTests(TestCase):

    def test_search(self):
        salida=duracionde.search("control")
        self.assertEqual(salida["lista"][0]["id"],"control")

class JuegosRestTests(TestCase):
    def test_listjuegos(self):
        response = self.client.get('/juegos/rest/v0/juegos/')
        self.assertEqual(response.status_code, 200)

import juegos.canales.basecom as basecom
class CanalbasecomTests(TestCase):

    def test_search(self):
        salida=basecom.search("")
        # self.assertTrue(salida)
    def test_detail(self):
        salida=basecom.detail("")
        # self.assertTrue(salida)
    def test_ofertas(self):
        salida=basecom.ofertas("")
        self.assertTrue(salida)
        salida=basecom.ofertas("nsw")
        self.assertTrue(salida)
        salida=basecom.ofertas("ps4")
        self.assertTrue(salida)
        salida=basecom.ofertas("ps5")
        self.assertTrue(salida)
    def test_trataPagina(self):
        ofertas={}
        ofertas['lista'] = []
        salida=basecom.trataPagina("https://www.base.com/games/playstation/bestseller/pg735/bn10009009/games.htm","?filter=a%3a568%3a385582&pgCMG735%2D2=3","ps4",ofertas)

import juegos.canales.tools as ctools
class CanalToolsTests(TestCase):

    def test_limpiatexto(self):
        cadena=ctools.limpiatexto("\t\n\t\n£")
        self.assertEqual(cadena,"")
        cadena=ctools.limpiatexto("")
        self.assertEqual(cadena,"")
        cadena=ctools.limpiatexto("a\t\nb\t\nc£d")
        self.assertEqual(cadena,"abcd")
    # def test_getexchangerate(self):
    #     salida=ctools.getexchangerate("GBP","EUR")

import juegos.canales.yambalu as yambalu
class CanalyambaluTests(TestCase):

    def test_search(self):
        salida=yambalu.search("")
        # self.assertTrue(salida)
    def test_detail(self):
        salida=yambalu.detail("")
        # self.assertTrue(salida)
    def test_ofertas(self):
        salida=yambalu.ofertas("")
        self.assertTrue(salida)
        salida=yambalu.ofertas("nsw")
        self.assertTrue(salida)
        salida=yambalu.ofertas("ps4")
        self.assertTrue(salida)
        salida=yambalu.ofertas("ps5")
        self.assertTrue(salida)
    def test_trataPagina(self):
        ofertas={}
        ofertas['lista'] = []
        salida=basecom.trataPagina("","","ps4",ofertas)

class OfertaModelTests(TestCase):
    def test_getconsola(self):
        oferta = Oferta(consola="nsw")
        self.assertEqual(oferta.getconsola(),"Switch")
        oferta.consola="ps4"
        self.assertEqual(oferta.getconsola(),"PS4")
        oferta.consola="ps5"
        self.assertEqual(oferta.getconsola(),"PS5")
        oferta= Oferta()
        self.assertEqual(oferta.getconsola(),"Sin texto")
        oferta= Oferta(consola="")
        self.assertEqual(oferta.getconsola(),"Sin texto")
        oferta= Oferta(consola="abc")
        self.assertEqual(oferta.getconsola(),"Sin texto")
