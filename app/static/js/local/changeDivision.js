function getDID(did){
    // var did = document.getElementById('did');
    console.log('This is did')
    console.log(did)
    if (did.value != 'None'){
      $.ajax({
          dataType : "json",
          url:"/admin/userManagement/changeDivisionChair/" + did,
          type:"GET",
          success:function(response){
            console.log(response)
            fillRemoveChairs(response);
          }
      })
    }
}

function fillRemoveChairs(response) {
  // get the selectpicker object
  var did = document.getElementById("did");
  // Remove all chairs from selectpicker
  $("#did option[value='divisionchair']").remove();
  // add the chairs from the response
  // refresh selectpicker
   $('.selectpicker').selectpicker('refresh');
}
