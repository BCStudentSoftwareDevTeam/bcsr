$("#Programs").hide();
$("#Divisions").hide();
$("#Add").hide();
$("#Remove").hide();
function show_access_level(s) {

        $("#Programs").hide();
        $("#Divisions").hide();
        $("#Add").hide();
        $("#Remove").hide();

        if (s == "program_chair"){
            $("#Programs").show();
            at = $("#accessType")
            at.val("program_chair");
            console.log($("#accessType").val())
        }
        else if (s == "division_chair"){
            $("#Divisions").show();
            at = $("#accessType")
            at.val("division_chair");
            console.log($("#accessType").val())

        }
        else if(s== "administrator"){
             retrieveAdmins();
             $("#Add").show();
             $("#Remove").show();
             at = $("#accessType")
             at.val("administrator");
             console.log($("#accessType").val())

        }
    }

function fillProgramChairs(response){
    console.log(response)
    var programselect = document.getElementById("RemoveDropdown");
    $("#RemoveDropdown").empty();
    var option = document.createElement("option");
    option.disabled = true;
    option.selected = true;
    option.text="---";
    option.value = "---";
    programselect.appendChild(option);

    for (var key in response){
        console.log(response[key]['firstname']);
        var option = document.createElement("option");
        option.text=response[key]["firstname"].toString()+" "+response[key]["lastname"].toString()+"(" + response[key]["username"].toString() + ")";
        option.value = key;
        programselect.appendChild(option); //adds the selected user to program chair list
    }
    $('.selectpicker').selectpicker('refresh');
}

function retrievePrograms(obj){
     var selected_program = obj.value;
     console.log(selected_program)
     if(selected_program){
         var url = '/admin/userManagement/get_program_chairs/'+selected_program;
         console.log("URL: " + url);
         $.ajax({
                url: url,
                dataType: 'json',
                success: function(response){
                    console.log(response)
          		    fillProgramChairs(response);
                  $("#Add").show();
                  $("#Remove").show();
          			}
                }); }
}

function program_chairs_show_names(s) { //Called in HTML
            retrievePrograms(s);

}

function fillDivisionChairs(response){
    var divisionselect = document.getElementById("RemoveDropdown");
    $("#RemoveDropdown").empty();
    var option = document.createElement("option");
    option.disabled = true;
    option.selected = true;
    option.text="---";
    option.value = "---";
    divisionselect.appendChild(option);
    for (var key in response){
        var option = document.createElement("option");
        option.text=response[key]["firstname"].toString()+" "+response[key]["lastname"].toString()+" ("+response[key]["username"].toString() + ")";
        option.value = key;
        divisionselect.appendChild(option); //adds the selected user to division chair
    }
    $('.selectpicker').selectpicker('refresh');
}

function retrieveDivisions(obj){
    console.log(obj.value)
    var selected_division = obj.value;
    if(selected_division){
        var url = '/admin/userManagement/get_division_chairs/'+selected_division;
         $.ajax({
                url: url,
                dataType: 'json',
                success: function(response){
          		    fillDivisionChairs(response);
          			},
          			error: function(error){
          				console.log(error);
          			}
                }); }
}

function division_chairs_show_names(s) { //Called in html
           retrieveDivisions(s);
           $("#Add").show();
           $("#Remove").show();
       }

function fillAdmin(response){
   var adminselect = document.getElementById("RemoveDropdown")
       $("#RemoveDropdown").empty();
       var count = 0;
       for (var key in response){
           count = count + 1;
           var option = document.createElement("option");
               option.text=response[key]["firstname"].toString()+" "+response[key]["lastname"].toString()+" ("+ response[key]["username"].toString() + ")";
               option.value = key;
               adminselect.appendChild(option); //adds the selected user as Admin
       }
       if (count < 2) {
           //disables the remove button if there is only one admin so that all the users are not locked out of the system
           var disable_btn = document.getElementById("adminbtn");
           disable_btn.disabled = true;
       }

   $('.selectpicker').selectpicker('refresh');
}

function retrieveAdmins(){
  // Getting the Admin
      $.ajax({
          dataType : "json",
          url:"/admin/userManagement/get_admin",
          type:"GET",
          success:function(response){
            console.log(response)
            fillAdmin(response);

          }
       });
}
