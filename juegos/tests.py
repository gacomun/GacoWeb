from django.test import TestCase
from django.urls import reverse

from .models import Juego

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

def create_juego(title):
    
    return Juego.objects.create(title=title)


class JuegoIndexViewTests(TestCase):
    def test_no_juegos(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('juegos:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No juegos are available.")
        self.assertQuerysetEqual(response.context['juego_list'], [])

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
    
    def test_searchgame(self):
        cadena=n.searchgame("overcooked")
        lista = json.loads(cadena)
        self.assertNotEqual(len(lista),0)

    def test_detail(self):        
        sal=n.detail("https://www.nintendo.es/Juegos/Nintendo-Switch/Overcooked-2-1388792.html")
        self.assertTrue(sal)
        detalle = json.loads(sal)
        self.assertNotEqual(detalle["tamano"],0)
        sal=n.detail("https://www.nintendo.es/Contenido-descargable/Overcooked-2-Surf-n-Turf-1454782.html")
        self.assertTrue(sal)
        detalle = json.loads(sal)
        self.assertNotEqual(detalle["tamano"],0)
        sal=n.detail("https://www.nintendo.es/Juegos/Programas-descargables-Nintendo-Switch/Coffee-Crisis-1468498.html")
        self.assertTrue(sal)
        detalle = json.loads(sal)
        self.assertNotEqual(detalle["tamano"],0)

import juegos.canales.hl2b as HLTB
class Canalhl2bTests(TestCase):

    def test_limpiatexto(self):
        cadena=HLTB.limpiatexto("\t\n\t\n")
        self.assertEqual(cadena,"")
        cadena=HLTB.limpiatexto("")
        self.assertEqual(cadena,"")
        cadena=HLTB.limpiatexto("a\t\nb\t\nc")
        self.assertEqual(cadena,"abc")

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
        self.assertEqual(jbbdd.image,None)
        self.assertEqual(jbbdd.tamano,0)

        jbbdd.consola="nsw"
        jbbdd.save()
        t.toolactualizajuegos()
        jbbdd = Juego.objects.get(id=0)
        self.assertNotEqual(jbbdd.image,None)
        self.assertNotEqual(jbbdd.tamano,0)

        jbbdd.tiempo=0
        jbbdd.save()
        t.toolactualizajuegos()
        jbbdd = Juego.objects.get(id=0)
        self.assertNotEqual(jbbdd.tiempo,0)


    def test_toolbuscajuegoswitch(self):
        juego = Juego(id=1,title="jdasdhas",consola="nsw")
        juego.save()
        t.toolbuscajuegoswitch(juego)
        juego = Juego.objects.get(id=1)
        self.assertEqual(juego.image,None)
        self.assertEqual(juego.tamano,0)
        juego.title="Coffee Crisis"
        t.toolbuscajuegoswitch(juego)
        juego = Juego.objects.get(id=1)
        self.assertNotEqual(juego.image,None)
        self.assertNotEqual(juego.tamano,0)

    def test_tooldetactualiza(self):
        juego = Juego(id=2)
        juego.save()
        t.tooldetactualiza(2,"https://www.nintendo.es/Juegos/Programas-descargables-Nintendo-Switch/Coffee-Crisis-1468498.html","ps4")
        juego = Juego.objects.get(id=2)
        self.assertEqual(juego.image,None)
        self.assertEqual(juego.tamano,0)
        t.tooldetactualiza(2,"https://www.nintendo.es/Juegos/Programas-descargables-Nintendo-Switch/Coffee-Crisis-1468498.html","nsw")
        juego = Juego.objects.get(id=2)
        self.assertNotEqual(juego.image,None)
        self.assertNotEqual(juego.tamano,0)

    def test_tooldetactualizatiempo(self):
        juego = Juego(id=3)
        juego.save()
        t.tooldetactualizatiempo(3,"/game?id=65442")
        juego = Juego.objects.get(id=3)
        self.assertNotEqual(juego.tiempo,0)

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
