function myFunction(valor,j) {
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
      if(flag){
          tr[i].style.display = "";
      }
      else {
          tr[i].style.display = "none";
      }
    }
  }