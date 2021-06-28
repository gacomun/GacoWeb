function procesaId(){
    document.getElementById("spinner").style="";
    var id = document.getElementById("id").value
    var settings = {
      "url": "/juegos/rest/v0/juegos/"+id,
      "method": "GET",
      "timeout": 0,
    };
    
    $.ajax(settings).done(function (response) {
      console.log(response);
      document.getElementById("image").src=response.image
      document.getElementById("title").value=response.title
      document.getElementById("tipo").value=response.tipo.descripcion
      document.getElementById("consola").value=response.consola.descripcion
      document.getElementById("estado").value=response.estado.descripcion
      document.getElementById("tamano").value=response.tamano
      document.getElementById("tiempo").value=response.tiempo
      document.getElementById("ratio").value=response.ratio
      document.getElementById("precio").value=response.precio
      document.getElementById("terminado").setAttribute("class","imgcancel");
      if(response.terminado){document.getElementById("terminado").setAttribute("class","imgchecked");}
      document.getElementById("visible").setAttribute("class","imgcancel");
      if(response.visible){document.getElementById("visible").setAttribute("class","imgchecked");}
      document.getElementById("venta").setAttribute("class","imgcancel");
      if(response.venta){document.getElementById("venta").setAttribute("class","imgchecked");}
      document.getElementById("idprecio").setAttribute("class","disabled");
      document.getElementById("idprecio").setAttribute("href","")
      if(response.idPrecio!=""){
          document.getElementById("idprecio").setAttribute("class","");
          document.getElementById("idprecio").setAttribute("href","https://es.webuy.com/product-detail/?id="+response.idPrecio)
        }
    }).fail(function(data, textStatus, xhr) {
        setMensaje("ERROR","Busqueda Incorrecta detalle",document.getElementById("msg"))
        //This shows status code eg. 403
        //This shows status message eg. Forbidden
        console.log(data.status, xhr);
    }).always(function() {
      document.getElementById("spinner").style="visibility: hidden"
    });
  }