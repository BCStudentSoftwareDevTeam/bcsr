$("#Programs").hide();
$("#Divisions").hide();
$("#Add").hide();
$("#Remove").hide();
console.log ("im here")
function show_access_level(s) {
        console.log(s);
        $("#Programs").hide();
        $("#Divisions").hide();
        $("#Add").hide();
        $("#Remove").hide();
        console.log(s)
        if (s == "program_chair"){

            $("#Programs").show();
        }
        else if (s == "division_chair"){
            $("#Divisions").show();
        }
        else if(s== "administrator"){
             retrieveAdmins();
             $("#Add").show();
             $("#Remove").show();
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
          			}
          			// error: function(error){
          			// 	console.log(error);
          			// }
                }); }
}

function program_chairs_show_names(s) { //Called in HTML
            retrievePrograms(s);
            $("#Add").show();
            $("#Remove").show();
}

function fillDivisionChairs(response){
    // console.log(response)
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
        // console.log("URL: " + url);
         $.ajax({
                url: url,
                dataType: 'json',
                success: function(response){
                    // console.log(response)
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
   // console.log(response)
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
            fillAdmin(response);
          }
       });
}


// function getDID(did){
//   // Getting the Division DID that has been clicked on in userManagementSidebar
//     if (did.value != 'None'){
//       $.ajax({
//           dataType : "json",
//           url:"/admin/userManagement/changeDivision" + did,
//           type:"GET",
//           success:function(response){
//             fillRemoveChairs(response, did);
//           }
//        });
//     }
// }
// function fillRemoveChairs(response, did) {
//   // get the selectpicker object
//   var chair_did = $("#divisionRemoveSelectpicker");
//   // Remove all chairs from selectpicker
//   chair_did.empty().append('<option selected="selected" value="0">Please Select</option>');
//   for (var i = 0; i < response[did].length; i++) {
//     // add the chairs from the response
//     chair_did.append('<option>'+response[did][i]+'</option>');
//   }
//   // refresh selectpicker
//    $('.selectpicker').selectpicker('refresh');
// }













// function programRemoveChairs(response, pid) {
//   var program_pid = $("#programRemoveSelectpicker")
//   program_pid.empty().append('<option selected="selected" value="0">Please Select</option>');
//   for (var i = 0; i < response[did].length; i++) {
//     program_pid.append('<option>'+response[pid][i]+'</option>');
//   }
//   // $('.selectpicker')
// }
