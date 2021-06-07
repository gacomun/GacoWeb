from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Juego
import juegos.tools as t

# class IndexView(generic.ListView):
#     template_name = 'juegos/index.html'
#     context_object_name = 'juego_list'

#     def get_queryset(self):
#         """Return the last five published questions."""
# #        return Juego.objects.all().filter(terminado=False).order_by('-tamano')
#         return sorted(Juego.objects.all().filter(visible=True), key= lambda j: j.getratio(), reverse=True)

def index(request):
    if request.method == "POST":
        juego_list = Juego.objects.all()
        titulo=request.POST['titulo']
        if titulo != "":
            juego_list=juego_list.filter(title__contains=titulo)
        ratio=request.POST['ratio']
        consola=request.POST['consola']
        if consola != "":
            juego_list=juego_list.filter(consola=consola)
        end=request.POST['end']
        if end != "":
            juego_list=juego_list.filter(terminado=end)
        venta=request.POST['venta']
        if venta != "":
            juego_list=juego_list.filter(venta=venta)
        visible=request.POST['visible']
        if visible != "":
            juego_list=juego_list.filter(visible=visible)
        order=request.POST['opciones']
        if order =="1":
            juego_list = juego_list.order_by("-title")
        elif order =="3":
            juego_list = juego_list.order_by("-tamano")
        elif order =="4":
            juego_list = juego_list.order_by("-tiempo")
        elif order =="5":
            juego_list = juego_list.order_by("-precio")
        else:    
            juego_list = sorted(juego_list, key= lambda j: j.getratio(), reverse=True)
        if ratio != "":
            juegos_temp=[]
            for juego in juego_list:
                if ratio in str(juego.getratio()):
                    juegos_temp.append(juego)
            juego_list=juegos_temp


    else:
        juego_list = sorted(Juego.objects.all().filter(visible=True), key= lambda j: j.getratio(), reverse=True)
    context = {
        'juego_list': juego_list,
    }
    return render(request, 'juegos/index.html', context)



class DetailView(generic.DetailView):
    model = Juego
    template_name = 'juegos/detail.html'


class ResultsView(generic.DetailView):
    model = Juego
    template_name = 'juegos/results.html'


def tools(request):
    context = {}
    return render(request, 'juegos/tools.html', context)


def carga(request):
    cookie=request.POST['cookie']
    if cookie=="":
        return render(request, 'juegos/tools.html', {'error_message': "Cookie obligatoria",})
    plataforma=request.POST['plataforma']
    try:
        if plataforma == 'nsw':
            t.toolcargaswitch(cookie)
        if plataforma == 'ps4':
            t.toolcargaps4(cookie)
    except: 
        # Redisplay the question voting form.
        return render(request, 'juegos/tools.html', {'error_message': "Error acceso",})
    else:
        return render(request, 'juegos/tools.html')
    
def actualiza(request):
    t.toolactualizajuegos()
    return render(request, 'juegos/tools.html')

def detactualiza(request, juego_id):
    url=request.POST['url']
    plataforma=request.POST['plataforma']
    t.tooldetactualiza(juego_id,url,plataforma)
    juego = get_object_or_404(Juego, pk=juego_id)
    return render(request, 'juegos/detail.html', {'juego': juego})

def detactualizatiempo(request, juego_id):
    url=request.POST['url']
    t.tooldetactualizatiempo(juego_id,url)
    juego = get_object_or_404(Juego, pk=juego_id)
    return render(request, 'juegos/detail.html', {'juego': juego})

def precios(request):
    t.toolpreciojuegos()
    return render(request, 'juegos/tools.html')
