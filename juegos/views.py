from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic, View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Juego
import juegos.tools as t
import juegos.canales.nintendo as n
import juegos.canales.sony as s
import juegos.canales.hl2b as HLTB



# class IndexView(generic.ListView):
#     template_name = 'juegos/index.html'
#     context_object_name = 'juego_list'

#     def get_queryset(self):
#         """Return the last five published questions."""
# #        return Juego.objects.all().filter(terminado=False).order_by('-tamano')
#         return sorted(Juego.objects.all().filter(visible=True), key= lambda j: j.getratio(), reverse=True)

def index(request):
    return render(request, 'juegos/index.html')



class DetailView(generic.DetailView):
    model = Juego
    template_name = 'juegos/detail.html'

def detail(request, pk):
    context = {
        'id': pk
    }
    return render(request, 'juegos/detail.html', context)

def tools(request):
    context = {}
    return render(request, 'juegos/tools.html', context)

# def detactualiza(request, juego_id):
#     url=request.POST['url']
#     plataforma=request.POST['plataforma']
#     t.tooldetactualiza(juego_id,url,plataforma)
#     juego = get_object_or_404(Juego, pk=juego_id)
#     return render(request, 'juegos/detail.html', {'juego': juego})

# def detactualizatiempo(request, juego_id):
#     url=request.POST['url']
#     t.tooldetactualizatiempo(juego_id,url)
#     juego = get_object_or_404(Juego, pk=juego_id)
#     return render(request, 'juegos/detail.html', {'juego': juego})


# def searchjuego(request):
#     respuesta={}
#     consola=""
#     if request.method == "POST":
#         titulo=request.POST['titulo']
#         if 'opciones' not in request.POST:
#             canal = "1"
#         else:
#             canal=request.POST['opciones']
#         if canal =="1":
#             respuesta=n.search(titulo)
#             consola="nsw"
#         elif canal =="2":
#             respuesta=s.search(titulo)
#             consola="ps4"
#         elif canal =="3":
#             respuesta=HLTB.search(titulo)
#         filtro={
#             'titulo':titulo,
#             'canal':canal
#         }

#     else:
#         filtro={
#                 'canal':"1"
#             }
#     context = {
#         'respuesta': respuesta,
#         'filtro': filtro,
#         'consola':consola
#     }
#     return render(request, 'juegos/searchjuego.html',context)


# def detsearchjuego(request, juego_id):
#     if request.method == "GET":
#         jbbdd = Juego.objects.get(id=juego_id)
#         respuesta={}
#         consola=""
#         filtro={
#             'canal':"3",
#             'titulo':jbbdd.title
#         }
#         context = {
#             'respuesta': respuesta,
#             'filtro': filtro,
#             'consola':consola
#         }
#         return render(request, 'juegos/searchjuego.html',context)

def canalsearch(request):
    # if request.method == "POST":
    #     modo=request.POST['modo']
    #     id=""
    #     if 'id' in request.POST:
    #         id=request.POST['id']
    #     context = {
    #         'modo': modo,
    #         'id': id
    #     }
    #     return render(request, 'juegos/searchjuego.html',context)
    if request.method == "GET":
        modo=""
        id=""
        if 'modo' in request.GET:
            modo=request.GET['modo']
        if 'id' in request.GET:
            id=request.GET['id']
        context = {
            'modo': modo,
            'id': id
        }
        return render(request, 'juegos/searchjuego.html',context)
