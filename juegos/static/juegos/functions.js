function myFunction(valor, j) {
  var input, filter, table, tr, td, i;
  //input = document.getElementById("myInput");
  filter = valor.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (var i = 1; i < tr.length; i++) {
    var tds = tr[i].getElementsByTagName("td");
    var flag = false;
    //      for(var j = 0; j < tds.length; j++){
    var td = tds[j];
    if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
      flag = true;
    }
    //      }
    if (flag) {
      tr[i].style.display = "";
    }
    else {
      tr[i].style.display = "none";
    }
  }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

function setMensaje(tipo,mensaje,donde){
  texto="";
  if(tipo=="OK"){
    // var cellText = document.createTextNode(texto);
    // cell.appendChild(cellText);
    texto='<div class="alert alert-success alert-dismissible fade show">'
    texto=texto.concat('<strong>Success!</strong> ').concat(mensaje)
    texto=texto.concat('<button type="button" class="close" data-dismiss="alert">&times;</button>')
    texto=texto.concat('</div>')
  } else if (tipo=="ERROR") {
    texto='<div class="alert alert-danger alert-dismissible fade show">'
    texto=texto.concat('<strong>Error!</strong> ').concat(mensaje)
    texto=texto.concat('<button type="button" class="close" data-dismiss="alert">&times;</button>')
    texto=texto.concat('</div>')
  } else if (tipo=="WARN") {
    texto='<div class="alert alert-warning alert-dismissible fade show">'
    texto=texto.concat('<strong>Warning!</strong> ').concat(mensaje)
    texto=texto.concat('<button type="button" class="close" data-dismiss="alert">&times;</button>')
    texto=texto.concat('</div>')
  } else if (tipo=="INFO") {
    texto='<div class="alert alert-info alert-dismissible fade show">'
    texto=texto.concat('<strong>Info!</strong> ').concat(mensaje)
    texto=texto.concat('<button type="button" class="close" data-dismiss="alert">&times;</button>')
    texto=texto.concat('</div>')
  }
  donde.innerHTML=texto
}

function crearcelda(texto,row,tipo,attrs){
  var cell = document.createElement(tipo);
  // var cellText = document.createTextNode(texto);
  // cell.appendChild(cellText);
  cell.innerHTML=texto
  attrs.forEach(element => {
    cell.setAttribute(element[0],element[1])
  });
  row.appendChild(cell);
  return cell;
}

function getRadioValue(name) {
  var ele = document.getElementsByName(name);
  var dev=""  
  for(i = 0; i < ele.length; i++) {
      if(ele[i].checked){
        dev=ele[i].value;
      }
  }
  return dev
}

function setRadioValue(name,valor) {
  var ele = document.getElementsByName(name);
  for(i = 0; i < ele.length; i++) {
      if(ele[i].value==valor){
        ele[i].checked=true;
      }
      else{
        ele[i].checked=false;
      }
  }
}
