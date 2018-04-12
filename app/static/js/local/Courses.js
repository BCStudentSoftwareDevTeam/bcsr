/* global Dropzone */
$(document).ready(function() {
    $('#courses').DataTable();
    Dropzone.autoDiscover = false;
});


function upload(CID){
   $("#uploadSyllabusModal").modal('toggle');
   var type = "syllabus"
   var new_url  = "/uploads/"+type+"/"+ CID
   console.log(new_url)
//   Dropzone.autoDiscover = false;
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
     accept: function(file, done) {
         done();
         console.log("File uploaded");
     }
   };
   Dropzone.autoDiscover = false;
   var MyDropzone = new Dropzone(uploader, dropzone_options);

}

function reload() {
    location.reload();
}



//To-DO: 

function uploadOptional(CID){
  $("#uploadOptionalModal").modal('toggle');
  var type = "other"
  var new_url  = "/uploads/"+type+"/"+ CID
//   Dropzone.autoDiscover = false;
  var uploader = document.querySelector('#dropOptional');
  var dropzone_options = {
     url: new_url,
     paramName: "file", // The name that will be used to transfer the file
     maxFilesize: 5, // MB
     maxFiles: 1,
     acceptedFiles: ".doc,.docx,.pdf,.txt, .zip",
     dictDefaultMessage: "Upload your additional materials here",
     uploadMultiple: false,
     addRemoveLinks: true,
     clickable: true,
     accept: function(file, done) {
         done();
         console.log("File uploaded");
     }
  };
  Dropzone.autoDiscover = false;
  var optionalDropzone = new Dropzone(uploader, dropzone_options);

}











































    // var length = $('[id="drop"]').length;
    // var counter = 0;
    // for (i = 0; i < length; i++){
    //     changeID(counter);
    //     counter++;
    // }
// function changeID(counter){
//     var element = document.getElementById("drop");
//     element.id = "element"+counter;
//     console.log("element"+counter)
//     console.log("Counter:" + counter);
// }

// function delete_syllabus(form_id) {
//     swal({
//         title: "Are you sure?",
//         text: "You will not be able to recover this file!",
//         type: "warning",
//         showCancelButton: true,
//         confirmButtonColor: "#DD6B55",
//         confirmButtonText: "Yes, delete it!",
//         closeOnConfirm: false
//     }, function() {
//          $(form_id).submit();
//     });
// };

// function showPrograms(division) {
//     var programID = '#programs-'+ division;
//     if($(programID).css('display') == 'none'){
//         $(programID).css('display', 'block');
        
        
//     } else {
//         $(programID).css('display', 'none');
//     }
    
//     $('#icon-'+ division).toggleClass('glyphicon-plus')
//     $('#icon-'+ division).toggleClass('glyphicon-minus')
// }


// function showCourses(program) {
//     var programID = '#courses-'+ program;
//     if($(programID).css('display') == 'none'){
//         $(programID).css('display', 'block');
        
        
//     } else {
//         $(programID).css('display', 'none');
//     }
    
//     $('#coursesIcon-'+ program).toggleClass('glyphicon-plus')
//     $('#coursesIcon-'+ program).toggleClass('glyphicon-minus')
// }
