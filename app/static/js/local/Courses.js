/* global Dropzone */
$(document).ready(function() {
    $('#courses').DataTable();
    Dropzone.autoDiscover = false;
});

window.onload = function(){
    var selectEl = document.getElementById('termSelect');
    $('select[id=termSelect]').val('{{current_term}}')
    $('.selectpicker').selectpicker('refresh')
};


function filterTable(SEID, filterType){
    if (filterType == 1){
        window.location.replace("/courses/"+SEID+"/allCourses")
    } 
    if (filterType == 2){
        window.location.replace("/courses/"+SEID+"/withSyllabus")
    }
     if (filterType == 3){
        window.location.replace("/courses/"+SEID+"/noSyllabus")
    }
}


function upload(CID){
   $("#uploadSyllabusModal").modal('toggle');
   var type = "syllabus"
   var new_url  = "/uploads/"+type+"/"+ CID
   var uploader = document.querySelector('#drop');
   var dropzone_options = {
     url: new_url,
     paramName: "file", // The name that will be used to transfer the file
     maxFilesize: 5, // MB
     maxFiles: 1,
     acceptedFiles: ".doc,.docx,.pdf,.txt, .zip",
     dictDefaultMessage: "Upload your syllabus here",
     uploadMultiple: false,
     addRemoveLinks: true,
     clickable: true,
     autoProcessQueue: false,
     accept: function(file, done) {
         done();
         console.log("File uploaded");
     }
   };
   Dropzone.autoDiscover = false;
   var MyDropzone = new Dropzone(uploader, dropzone_options);
   var submitButton = document.querySelector("#submitSyllabus")
    submitButton.addEventListener("click", function() {
      MyDropzone.processQueue(); // Tell Dropzone to process all queued files.
      console.log("The queue for syllabus was processed")
      location.reload();
    });
 

}





function uploadOptional(CID){
  $("#uploadOptionalModal").modal('toggle');
  var type = "other"
  var new_url  = "/uploads/"+type+"/"+ CID

  var uploader = document.querySelector('#dropOptional');
  var dropzone_options = {
     url: new_url,
     paramName: "file", // The name that will be used to transfer the file
     maxFilesize: 5, // MB
     maxFiles: 100,
     acceptedFiles: ".doc,.docx,.pdf,.txt, .zip",
     dictDefaultMessage: "Upload your additional materials here",
     uploadMultiple: false,
     addRemoveLinks: true,
     clickable: true,
     autoProcessQueue: false,
     accept: function(file, done) {
         done();
         console.log("File uploaded");
     }
  };
  Dropzone.autoDiscover = false;
  var optionalDropzone = new Dropzone(uploader, dropzone_options);
     var submitButton = document.querySelector("#submitOptional")
     submitButton.addEventListener("click", function() {
      optionalDropzone.processQueue(); // Tell Dropzone to process all queued files.
      console.log("The queue for optional was processed!")
      location.reload();
    });
 
}




