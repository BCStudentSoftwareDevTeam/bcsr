function Division_page_load(){
  $.ajax({
      dataType : "json",
      url:"/admin/userManagement/changeDivisionChair/",
      type:"GET",
      success:function(response){
         return (response)
      }
   });
}


function getDID(did){
  // Getting the Division DID that has been clicked on in userManagementSidebar
    if (did.value != 'None'){
      $.ajax({
          dataType : "json",
          url:"/admin/userManagement/changeDivisionChair/" + did,
          type:"GET",
          success:function(response){
            fillRemoveChairs(response, did);
          }
       });
    }
}


function fillRemoveChairs(response, did) {
  // get the selectpicker object
  var chair_did = $("#divisionRemoveSelectpicker");
  // Remove all chairs from selectpicker
  chair_did.empty().append('<option selected="selected" value="0">Please Select</option>');
  for (var i = 0; i < response[did].length; i++) {
    // add the chairs from the response
    chair_did.append('<option>'+response[did][i]+'</option>');
  }
  // refresh selectpicker
   $('.selectpicker').selectpicker('refresh');
}


function programRemoveChairs(response, pid) {
  var program_pid = $("#programRemoveSelectpicker")
  program_pid.empty().append('<option selected="selected" value="0">Please Select</option>');
  for (var i = 0; i < response[did].length; i++) {
    program_pid.append('<option>'+response[pid][i]+'</option>');
  }
  // $('.selectpicker')
}
