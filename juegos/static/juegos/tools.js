function tools_carga(){
    document.getElementById("spinner").style=""
    var plataforma = document.getElementById("plataforma").value
    var cookie = document.getElementById("cookie").value
    csrftoken = getCookie('csrftoken');
    var settings = {
        "url": "/juegos/rest/v0/tools/carga",
        "method": "POST",
        "timeout": 0,
        "headers": {
          "Content-Type": "application/json",
          'X-CSRFToken': csrftoken
        },
        "data": JSON.stringify({
          "cookie": cookie,
          "plataforma": plataforma
        }),
      };
      
      $.ajax(settings).done(function (response) {
        msg=response.message;
        setMensaje("OK",msg,document.getElementById("msg"))
      }).fail(function(data, textStatus, xhr) {
        var msg="Carga Incorrecta."          
        if (data.status != 500){
          msg=data.responseJSON.message;
        }
        setMensaje("ERROR",msg,document.getElementById("msg"))
        //This shows status code eg. 403
        //This shows status message eg. Forbidden
        console.log(data.status, xhr);
        }).always(function() {
            document.getElementById("spinner").style="visibility: hidden"
        });
}

function tools_actualiza(){
    document.getElementById("spinner").style=""
    var settings = {
        "url": "/juegos/rest/v0/tools/actualiza",
        "method": "GET",
        "timeout": 0,
      };
      
      $.ajax(settings).done(function (response) {
        msg=response.message;
        setMensaje("OK",msg,document.getElementById("msg"))
      }).fail(function(data, textStatus, xhr) {
        var msg="Actualización Incorrecta."          
        if (data.status != 500){
          msg=data.responseJSON.message;
        }
        setMensaje("ERROR",msg,document.getElementById("msg"))
        //This shows status code eg. 403
        //This shows status message eg. Forbidden
        console.log(data.status, xhr);
        }).always(function() {
            document.getElementById("spinner").style="visibility: hidden"
        });
}

function tools_precios(){
    document.getElementById("spinner").style=""
    var settings = {
        "url": "/juegos/rest/v0/tools/precios",
        "method": "GET",
        "timeout": 0,
      };
      
      $.ajax(settings).done(function (response) {
        msg=response.message;
        setMensaje("OK",msg,document.getElementById("msg"))
      }).fail(function(data, textStatus, xhr) {
        var msg="Actualización Incorrecta."          
        if (data.status != 500){
          msg=data.responseJSON.message;
        }
        setMensaje("ERROR",msg,document.getElementById("msg"))
        //This shows status code eg. 403
        //This shows status message eg. Forbidden
        console.log(data.status, xhr);
        }).always(function() {
            document.getElementById("spinner").style="visibility: hidden"
        });
}