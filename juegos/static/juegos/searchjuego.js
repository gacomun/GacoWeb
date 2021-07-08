function listcanal() {
    document.getElementById("spinner").style="";
    var canal = getRadioValue("opciones")
    var titulo = document.getElementById("titulo").value
    var settings = {
      "url": "/juegos/rest/v0/canales/"+canal+"?title="+titulo,
      "method": "GET",
      "timeout": 0,
    };
    $.ajax(settings).done(function (response) {
      tableCreate(response.lista);
    //   setMensaje("OK","Busqueda Correcta",document.getElementById("msg"))
    }).fail(function(data, textStatus, xhr) {
        setMensaje("ERROR","Busqueda Incorrecta",document.getElementById("msg"))
        //This shows status code eg. 403
        //This shows status message eg. Forbidden
        console.log(data.status, xhr);
   }).always(function() {
      document.getElementById("spinner").style="visibility: hidden"
    });
  }
  
  function tableCreate(lista) {
    //body reference 
    $("#tabla").remove(); 
    

    var body = document.getElementsByTagName("body")[0];
  
    // create elements <table> and a <tbody>
    var tbl = document.createElement("table");
    tbl.setAttribute("class","table table-info table-striped table-sm");
    tbl.setAttribute("id","tabla");
    var tblBody = document.createElement("tbody");
    var row = document.createElement("tr");
    crearcelda("Titulo",row,"th",[["scope","col"]])
    crearcelda("Imagen",row,"th",[["scope","col"]])
    crearcelda("Resumen",row,"th",[["scope","col"]])
    crearcelda("Detail",row,"th",[["scope","col"]])
    tblBody.appendChild(row);
    // cells creation
    if (lista){

      for (var j = 0; j < lista.length; j++) {
        // table row creation
        row = document.createElement("tr");
        crearcelda("<a href='"+lista[j].detail+"'>"+lista[j].titulo+"</a>",row,"td",[])
        crearcelda('<img src="'+lista[j].thumb+'" class="img-thumbnail" width="100">',row,"td",[])
      //   lista[j].tiempos
        crearcelda(getResumen(lista[j],j),row,"td",[])

        crearcelda(getDetail(j,lista[j]),row,"td",[])
        //row added to end of table body
        tblBody.appendChild(row);
      }
    }
  
    // append the <tbody> inside the <table>
    tbl.appendChild(tblBody);
    // put <table> in the <body>
    body.appendChild(tbl);
    // tbl border attribute to 
    // tbl.setAttribute("border", "2");
  }
  

  function getResumen(lista,numero) {
    var modo = document.getElementById("modo").value
    var dev="";
    if(modo == "tiempo")
    {
        for(i = 0; i < lista.tiempos.length; i++) {
            // dev+="<input type='radio' id='"+lista[i].clave+"' name='"+lista[i].clave+"' value='"+lista[i].clave+"'>";
            // dev+="<label>"+lista[i].clave+" = "+lista[i].valor +"</label><br>"
            clave=lista.tiempos[i].clave;
            valor=lista.tiempos[i].valor;
            dev=dev.concat('<input class="form-check-input" type="radio" name="tiempo').concat(numero).concat('" id="').concat(clave).concat('" value="').concat(valor).concat('" onclick=clicktiempo(').concat(numero).concat(',').concat(valor).concat(')>')
            dev=dev.concat('<label class="form-check-label" for="flexRadioDefault1">').concat(clave).concat(' = ').concat(valor).concat('</label><br>')
        }
        dev+="";
    }else if(modo == "precio"){
      dev=dev.concat('<ul class="list-group">');
      for(i = 0; i < lista.precios.length; i++) {
        clave=lista.precios[i].clave;
        valor=lista.precios[i].valor;
        dev=dev.concat('<li class="list-group-item list-group-item-warning">').concat(clave).concat(" -> ").concat(valor).concat('</li>');
      }
    }else if(modo == "alta"){
      dev=dev.concat("Consola -> ").concat(lista.consola)
    }
    dev=dev.concat('</ul>');
    return dev
  }

function procesarTiempo(numero) {
    document.getElementById("spinner").style="";
    var id = document.getElementById("id").value
    var tiempo = document.getElementById("tiempo"+numero).value
    csrftoken = getCookie('csrftoken');
    var settings = {
        "url": "/juegos/rest/v0/juegos/"+id,
        "csrfmiddlewaretoken":window.CSRF_TOKEN,
        "method": "PATCH",
        "timeout": 0,
        "headers": {
          "Content-Type": "application/json",
          'X-CSRFToken': csrftoken
        },
        "data": JSON.stringify({
          "tiempo": tiempo
        }),
      };
      
      $.ajax(settings).done(function (response) {
        console.log(response);
        setMensaje("OK","Tiempo juego actualizado",document.getElementById("msg"))
      }).fail(function(data, textStatus, xhr) {
        setMensaje("ERROR","Actualizando Juego",document.getElementById("msg"))
        //This shows status code eg. 403
        //This shows status message eg. Forbidden
        console.log(data.status, xhr);
   }).always(function() {
      document.getElementById("spinner").style="visibility: hidden"
    });
}

function getDetail(numero,elemento) {
    var dev="";
    //'Tipo<select class="form-select form-select-sm" id="tipo" name="tipo"><option value="d" selected="selected">Digital</option><option value="f" >Fisico</option></select>Estado<select class="form-select form-select-sm" id="estado" name="estado"><option value="n">Nuevo</option><option value="u" selected="selected">Usado</option></select><button type="submit" class="btn btn-primary" onclick="procesar()">Procesar</button>'
    var modo = document.getElementById("modo").value
    if(modo == "tiempo")
    {
        dev+='<input type="hidden" name="tiempo'+numero+'" id="tiempo'+numero+'" value=""><button type="submit" class="btn btn-primary" onclick="procesarTiempo('+numero+')">Procesar</button>';
    } else if(modo == "alta"){
      dev=dev.concat('<input type="hidden" name="titulo'+numero+'" id="titulo'+numero+'" value="'+elemento.titulo+'">');
      dev=dev.concat('<input type="hidden" name="idExterno'+numero+'" id="idExterno'+numero+'" value="'+elemento.id+'">');
      dev=dev.concat('<input type="hidden" name="detail'+numero+'" id="detail'+numero+'" value="'+elemento.detail+'">');
      dev=dev.concat('<input type="hidden" name="imagen'+numero+'" id="imagen'+numero+'" value="'+elemento.thumb+'">');
      dev=dev.concat('<input type="hidden" name="consola'+numero+'" id="consola'+numero+'" value="'+elemento.consola+'">');
      dev=dev.concat('Tipo<select class="form-select form-select-sm" id="tipo'+numero+'" name="tipo'+numero+'"><option value="d" selected="selected">Digital</option><option value="f" >Fisico</option></select>');
      dev=dev.concat('Estado<select class="form-select form-select-sm" id="estado'+numero+'" name="estado'+numero+'"><option value="n">Nuevo</option><option value="u" selected="selected">Usado</option></select>');
      dev=dev.concat('<button type="submit" class="btn btn-primary" onclick="procesarAlta('+numero+')">Procesar</button>')
    } else if(modo == "buscar"){
        dev+='<input type="hidden" name="detalle'+numero+'" id="detalle'+numero+'" value="'+elemento.detail+'"><button type="submit" class="btn btn-primary" onclick="procesarBuscar('+numero+')">Procesar</button>';
    } else if(modo == "precio"){
        dev+='<button type="submit" class="btn btn-primary" onclick="procesarPrecio('+elemento.id+','+elemento.precios[0].valor+')">Procesar</button>';
    }
    return dev
  }
  function clicktiempo(numero,valor){
    document.getElementById("tiempo"+numero).value=valor
  }

  function procesarAlta(numero) {
    document.getElementById("spinner").style="";
    csrftoken = getCookie('csrftoken');
    var titulo = document.getElementById("titulo"+numero).value
    var idExterno = document.getElementById("idExterno"+numero).value
    var detail = document.getElementById("detail"+numero).value
    var imagen = document.getElementById("imagen"+numero).value
    var consola = document.getElementById("consola"+numero).value
    var tipo = document.getElementById("tipo"+numero).value
    var estado = document.getElementById("estado"+numero).value
    var settings = {
      "url": "/juegos/rest/v0/juegos/",
      "method": "POST",
      "timeout": 0,
      "headers": {
        "Content-Type": "application/json",
        'X-CSRFToken': csrftoken
      },
      "data": JSON.stringify({
        "titulo": titulo,
        "idExterno": idExterno,
        "detail": detail,
        "imagen": imagen,
        "consola": consola,
        "tipo":tipo,
        "estado":estado
      }),
    };
    
    $.ajax(settings).done(function (response) {
      // console.log(response);
      setMensaje("OK","Juego Añadido",document.getElementById("msg"))
    }).fail(function(data, textStatus, xhr) {
      setMensaje("ERROR","Error Añadiendo Juego",document.getElementById("msg"))
      //This shows status code eg. 403
      //This shows status message eg. Forbidden
      console.log(data.status, xhr);
    }).always(function() {
      document.getElementById("spinner").style="visibility: hidden"
    });
  }

  function procesaId(){
    var id = document.getElementById("id").value
    if(id!=""){
      document.getElementById("spinner").style="";
      var modo = document.getElementById("modo").value
      var settings = {
        "url": "/juegos/rest/v0/juegos/"+id,
        "method": "GET",
        "timeout": 0,
      };
      
      $.ajax(settings).done(function (response) {
        console.log(response);
        document.getElementById("titulo").value=response.title
        if (modo== "buscar"){
          canal=""
          if(response.consola.id=="nsw"){canal="nintendo"}
          else if (response.consola.id=="ps4") {canal="sony"}
          setRadioValue("opciones",canal)
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
  }

function procesarBuscar(numero) {
  document.getElementById("spinner").style="";
  var detail = document.getElementById("detalle"+numero).value
  var id = document.getElementById("id").value
  csrftoken = getCookie('csrftoken');

  var settings = {
    "url": "/juegos/rest/v0/juegos/"+id+"/actualiza",
    "method": "POST",
    "timeout": 0,
    "headers": {
      "Content-Type": "application/json",
      'X-CSRFToken': csrftoken
    },
    "data": JSON.stringify({
      "detalle": detail
    }),
  };
  
  $.ajax(settings).done(function (response) {
    // console.log(response);
    setMensaje("OK","Juego Actualizado",document.getElementById("msg"))
  }).fail(function(data, textStatus, xhr) {
    setMensaje("ERROR","Error Actualización",document.getElementById("msg"))
    //This shows status code eg. 403
    //This shows status message eg. Forbidden
    console.log(data.status, xhr);
  }).always(function() {
    document.getElementById("spinner").style="visibility: hidden"
  });
}

function procesarPrecio(idPrecio,precio) {
  document.getElementById("spinner").style="";
  var id = document.getElementById("id").value
  csrftoken = getCookie('csrftoken');
  var settings = {
      "url": "/juegos/rest/v0/juegos/"+id,
      "csrfmiddlewaretoken":window.CSRF_TOKEN,
      "method": "PATCH",
      "timeout": 0,
      "headers": {
        "Content-Type": "application/json",
        'X-CSRFToken': csrftoken
      },
      "data": JSON.stringify({
        "precio": precio,
        "idPrecio": idPrecio
      }),
    };
    
    $.ajax(settings).done(function (response) {
      console.log(response);
      setMensaje("OK","Precio juego actualizado",document.getElementById("msg"))
    }).fail(function(data, textStatus, xhr) {
      setMensaje("ERROR","Actualizando Precio Juego",document.getElementById("msg"))
      //This shows status code eg. 403
      //This shows status message eg. Forbidden
      console.log(data.status, xhr);
 }).always(function() {
    document.getElementById("spinner").style="visibility: hidden"
  });
}