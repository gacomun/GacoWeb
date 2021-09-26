from django.http import JsonResponse
from .models import Juego,Oferta 
from rest_framework.decorators import api_view
from rest_framework import status
import importlib
from django.shortcuts import get_object_or_404
import juegos.tools as t
import logging

# Create a logger for this file
logger = logging.getLogger(__file__)

@api_view(['GET', 'POST', 'DELETE'])
def juego_list(request):
    if request.method == 'GET':
        logger.info("Inicio listJuegos")
        items = Juego.objects.all()
        # items_data = serializers.serialize("json", Juego.objects.all())

        title = request.query_params.get('title', None)
        if title is not None:
            items=items.filter(title__contains=title)
        tipo=request.query_params.get('tipo', None)
        if tipo is not None:
            items=items.filter(tipo=tipo)
        consola=request.query_params.get('consola', None)
        if consola is not None:
            items=items.filter(consola=consola)
        end=request.query_params.get('end', None)
        if end is not None:
            items=items.filter(terminado=end)
        venta=request.query_params.get('venta', None)
        if venta is not None:
            items=items.filter(venta=venta)
        visible=request.query_params.get('visible', None)
        if visible is not None:
            items=items.filter(visible=visible)
        order=request.query_params.get('$orderby', None)
        if order is not None:
            if "ratio" in order:
                ratioord=False
                if " desc" in order:
                    ratioord=True
                items = sorted(items, key= lambda j: j.getratio(), reverse=ratioord)
            else:
                direccion="-"
                order = order.replace(" desc", "")
                if " asc" in order:
                    direccion=""
                    order = order.replace(" asc", "")
                items = items.order_by(direccion+order)
        ratio = request.query_params.get('ratio', None)
        if ratio is not None:
            juegos_temp=[]
            for juego in items:
                if ratio in str(juego.getratio()):
                    juegos_temp.append(juego)
            items=juegos_temp
        items_count = len(items)
        items_data = []
        for item in items:
            items_data.append(item.toJson())

        data = {
            'count': items_count,
            'items': items_data
        }

        return JsonResponse(data)
    if request.method == 'POST':
        logger.info("postJuego")
        j=Juego()
        error = ""
        if 'titulo' in request.data:
            j.title=request.data['titulo']
        else:
            error+='titulo,'
        if 'idExterno' in request.data:
            j.idexterno=request.data['idExterno']
        else:
            error+='idExterno,'
        if 'imagen' in request.data:
            imagen=request.data['imagen']
            j.imagen=imagen
        if 'consola' in request.data:
            j.consola=request.data['consola']
            if j.isValidConsola() == False :
                error+='valor consola no valida,'
        else:
            error+='consola,'
        if 'tipo' in request.data:
            j.tipo=request.data['tipo']
        if 'estado' in request.data:
            j.estado=request.data['estado']
        if 'detail' in request.data:
            detalle=request.data['detail']
        if error == "":
            j.save()
            if 'detail' in request.data:
                detalle=request.data['detail']
                t.tooldetactualiza(j.id,detalle,j.consola)
                j = get_object_or_404(Juego, pk=j.id)
                if 'imagen' in request.data:
                    j.image=imagen
                    j.save()
            data = {
                "message": "Juego creado"
            }
            return JsonResponse(data, status=201)
        else:
            data = {
                "message": "Error en creación de Juego: Campos obligatorios "+error
            }
            return JsonResponse(data, status=400)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def juego_detail(request, pk):
    try: 
        item = Juego.objects.get(pk=pk) 
    except Juego.DoesNotExist: 
        return JsonResponse({'message': 'El juego no existe'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET':
        logger.info("getJuego")
        items_data=item.toJson()
        return JsonResponse(items_data, status=200)
    elif request.method == 'PATCH':
        logger.info("patchJuego")
        if 'tiempo' in request.data:
            tiempo = request.data["tiempo"]
            item.tiempo=tiempo
        if 'idPrecio' in request.data:
            idPrecio = request.data["idPrecio"]
            item.idPrecio=idPrecio
        if 'precio' in request.data:
            precio = request.data["precio"]
            item.precio=precio
        item.save()
        return JsonResponse({'message': 'El juego "'+item.title+'" actualizado'}, status=200) 
    return JsonResponse({'message': 'Opción no implementada'}, status=status.HTTP_404_NOT_FOUND) 
@api_view(['GET'])
def canal_detail(request, canal):
    if request.method == 'GET':
        logger.info("listCanales")
        title = request.query_params.get('title', None)
        object = importlib.import_module("juegos.canales."+canal)
        result = object.search(title)
    return JsonResponse(result, status=200)


@api_view(['POST'])
def tools_carga_list(request):
    error=""
    cookie=""
    if 'cookie' in request.data:
        cookie=request.data['cookie']
        if cookie == "":
            error += " cookie,"
    else:
        error += " cookie,"
    plataforma=""
    if 'plataforma' in request.data:
        plataforma=request.data['plataforma']
    else:
        error += " plataforma,"
    if error != "":
        data = {
                "message": "Error en carga de juegos: Campos obligatorios "+error
            }
        return JsonResponse(data, status=400)
    try:
        if plataforma == 'nsw':
            t.toolcargaswitch(cookie)
        elif plataforma == 'ps4':
            t.toolcargaps4(cookie)
        else:
            data = {"message": "Error en carga de juegos: Plataforma '"+plataforma+"' no conocida"}
            return JsonResponse(data, status=400)
        data = {"message": "Carga realizada correctamente."}
        return JsonResponse(data, status=200)


    except: 
        msg="Error en carga de juegos: Error tecnico"
        logger.exception(msg)
        data = {"message": msg}
        return JsonResponse(data, status=500)

@api_view(['GET'])
def tools_actualiza_list(request):
    try:
        t.toolactualizajuegos()
        data = {"message": "Actualización realizada correctamente."}
        return JsonResponse(data, status=200)
    except: 
        msg="Error en actualización de juegos: Error tecnico"
        logger.exception(msg)
        data = {"message": msg}
        return JsonResponse(data, status=500)

@api_view(['GET'])
def tools_precios_list(request):
    try:
        t.toolpreciojuegos()
        data = {"message": "Actualización Precios realizada correctamente."}
        return JsonResponse(data, status=200)
    except: 
        msg="Error en actualización de precios: Error tecnico"
        logger.exception(msg)
        data = {"message": msg}
        return JsonResponse(data, status=500)

@api_view(['POST'])
def juego_detail_actualiza(request, pk):
    if request.method == 'POST':
        if 'detalle' in request.data:
            try: 
                item = Juego.objects.get(pk=pk) 
            except Juego.DoesNotExist: 
                msg='El juego no existe'
                logger.exception(msg)
                return JsonResponse({'message': msg}, status=status.HTTP_404_NOT_FOUND) 
            t.tooldetactualiza(pk,request.data["detalle"],item.consola)
            data = {"message": "Actualización Juego realizada correctamente."}
            return JsonResponse(data, status=200)
        else:
            data = {"message": "Error en actualizar juego: Campo obligatorio detalle"}
            return JsonResponse(data, status=400)

@api_view(['GET'])
def ofertas_list(request):
    if request.method == 'GET':
        logger.info("Inicio listOfertas")
        items = Oferta.objects.all()
        title = request.query_params.get('title', None)
        if title is not None:
            items=items.filter(title__contains=title)
        # canal=request.query_params.get('canal', None)
        # if canal is not None:
        #     items=items.filter(canal=int(canal))
        consola=request.query_params.get('consola', None)
        if consola is not None:
            items=items.filter(consola=consola)
        order=request.query_params.get('$orderby', None)
        if order is not None:
            direccion="-"
            order = order.replace(" desc", "")
            if " asc" in order:
                direccion=""
                order = order.replace(" asc", "")
            items = items.order_by(direccion+order)
        items_count = len(items)
        items_data = []
        for item in items:
            items_data.append(item.toJson())
        data = {
            'count': items_count,
            'items': items_data
        }
        return JsonResponse(data)

@api_view(['GET'])
def tools_ofertas_list(request):
    try:
        canal = request.query_params.get('canal', None)
        if canal is None:
            canal=""
        t.toolofertas(canal)
        data = {"message": "Actualización Ofertas realizada correctamente."}
        return JsonResponse(data, status=200)
    except: 
        msg="Error en actualización de ofertas: Error tecnico"
        logger.exception(msg)
        data = {"message": msg}
        return JsonResponse(data, status=500)