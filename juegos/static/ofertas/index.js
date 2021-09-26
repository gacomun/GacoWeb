function listofertas() {
    document.getElementById("spinner").style="";
    var filtro="";

    var titulo = document.getElementById("titulo").value;
    if(titulo!= ""){
      filtro=filtro.concat("title=").concat(titulo).concat("&");
    }
    var consola = document.getElementById("consola").value;
    if(consola!= ""){
      filtro=filtro.concat("consola=").concat(consola).concat("&");
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
        "url": "/juegos/rest/v0/ofertas/?"+filtro,
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
    crearcelda("Base.com Precio",row,"th",[["scope","col"]])
    crearcelda("Base.com Descuento",row,"th",[["scope","col"]])
    crearcelda("Yambalu Precio",row,"th",[["scope","col"]])
    crearcelda("Yambalu Descuento",row,"th",[["scope","col"]])
    crearcelda("Consola",row,"th",[["scope","col"]])

    tblBody.appendChild(row);
    // cells creation
    if (lista){
      for (var j = 0; j < lista.length; j++) {
        // table row creation
        row = document.createElement("tr");
        crearcelda(lista[j].title,row,"td",[])
        crearcelda('<img src="'+lista[j].image+'" class="img-thumbnail" width="100">',row,"td",[])
        crearcelda('<a href="'+lista[j].basecom.detail+'">'+lista[j].basecom.precio+' €</a>',row,"td",[])
        crearcelda(lista[j].basecom.descuento+" %",row,"td",[])
        crearcelda('<a href="'+lista[j].yambalu.detail+'">'+lista[j].yambalu.precio+' €</a>',row,"td",[])
        crearcelda(lista[j].yambalu.descuento+" %",row,"td",[])
        crearcelda(lista[j].consola.descripcion,row,"td",[])

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