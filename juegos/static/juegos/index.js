function listjuegos() {
  document.getElementById("spinner").style="";
  var filtro="";
  var titulo = document.getElementById("titulo").value;
  if(titulo!= ""){
    filtro=filtro.concat("title=").concat(titulo).concat("&");
  }
  var ratio = document.getElementById("ratio").value;
  if(ratio!= ""){
    filtro=filtro.concat("ratio=").concat(ratio).concat("&");
  }
  var tipo = document.getElementById("tipo").value;
  if(tipo!= ""){
    filtro=filtro.concat("tipo=").concat(tipo).concat("&");
  }
  var consola = document.getElementById("consola").value;
  if(consola!= ""){
    filtro=filtro.concat("consola=").concat(consola).concat("&");
  }
  var end = document.getElementById("end").value;
  if(end!= ""){
    filtro=filtro.concat("end=").concat(end).concat("&");
  }
  var venta = document.getElementById("venta").value;
  if(venta!= ""){
    filtro=filtro.concat("venta=").concat(venta).concat("&");
  }
  var visible = document.getElementById("visible").value;
  if(visible!= ""){
    filtro=filtro.concat("visible=").concat(visible).concat("&");
  }
  var order = getRadioValue("opciones");
  if(order!= ""){
    filtro=filtro.concat("$orderby=").concat(order).concat("");
  }
  var updown = getRadioValue("updown");
  if(updown!= ""){
    filtro=filtro.concat(updown).concat("&");
  }
  
    var settings = {
        "url": "/juegos/rest/v0/juegos/?"+filtro,
        "method": "GET",
        "timeout": 0,
      };
      
      $.ajax(settings).done(function (response) {
        tableCreate(response.items);
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
    crearcelda("Ratio",row,"th",[["scope","col"]])
    crearcelda("Tamaño",row,"th",[["scope","col"]])
    crearcelda("Tiempo",row,"th",[["scope","col"]])
    crearcelda("Tipo",row,"th",[["scope","col"]])
    crearcelda("Consola",row,"th",[["scope","col"]])
    crearcelda("Terminado",row,"th",[["scope","col"]])
    crearcelda("Venta",row,"th",[["scope","col"]])
    crearcelda("Precio",row,"th",[["scope","col"]])
    tblBody.appendChild(row);
    // cells creation
    if (lista){
      for (var j = 0; j < lista.length; j++) {
        // table row creation
        row = document.createElement("tr");
        crearcelda('<a href="/juegos/'+lista[j].id+'">'+lista[j].title+'</a>',row,"td",[])
        crearcelda('<img src="'+lista[j].image+'" class="img-thumbnail" width="100">',row,"td",[])
        crearcelda(lista[j].ratio,row,"td",[])
        crearcelda(lista[j].tamano+" MB",row,"td",[])
        crearcelda(lista[j].tiempo+" H",row,"td",[])
        crearcelda(lista[j].tipo.descripcion,row,"td",[])
        crearcelda(lista[j].consola.descripcion,row,"td",[])
        imgt='imgcancel'
        if(lista[j].terminado == true){
          imgt='imgchecked'
        }
        crearcelda('<img class="'+imgt+'" width="24">',row,"td",[])
        imgt='imgcancel'
        if(lista[j].venta == true){
          imgt='imgchecked'
        }
        crearcelda('<img class="'+imgt+'" width="24">',row,"td",[])
        crearcelda(lista[j].precio,row,"td",[])

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