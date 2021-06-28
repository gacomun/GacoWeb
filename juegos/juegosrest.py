from django.http import JsonResponse
from .models import Juego 
from rest_framework.decorators import api_view
from rest_framework import status
import importlib
from django.shortcuts import get_object_or_404
import juegos.tools as t




@api_view(['GET', 'POST', 'DELETE'])
def juego_list(request):
    if request.method == 'GET':
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
        items_data=item.toJson()
        return JsonResponse(items_data, status=200)
    elif request.method == 'PATCH':
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
        data = {
                "message": "Error en carga de juegos: Error tecnico"
            }
        return JsonResponse(data, status=500)

@api_view(['GET'])
def tools_actualiza_list(request):
    try:
        t.toolactualizajuegos()
        data = {"message": "Actualización realizada correctamente."}
        return JsonResponse(data, status=200)
    except: 
        data = {"message": "Error en actualización de juegos: Error tecnico"}
        return JsonResponse(data, status=500)

@api_view(['GET'])
def tools_precios_list(request):
    try:
        t.toolpreciojuegos()
        data = {"message": "Actualización Precios realizada correctamente."}
        return JsonResponse(data, status=200)
    except: 
        data = {"message": "Error en actualización de precios: Error tecnico"}
        return JsonResponse(data, status=500)

@api_view(['POST'])
def juego_detail_actualiza(request, pk):
    if request.method == 'POST':
        if 'detalle' in request.data:
            try: 
                item = Juego.objects.get(pk=pk) 
            except Juego.DoesNotExist: 
                return JsonResponse({'message': 'El juego no existe'}, status=status.HTTP_404_NOT_FOUND) 
            t.tooldetactualiza(pk,request.data["detalle"],item.consola)
            data = {"message": "Actualización Juego realizada correctamente."}
            return JsonResponse(data, status=200)
        else:
            data = {"message": "Error en actualizar juego: Campo obligatorio detalle"}
            return JsonResponse(data, status=400)
