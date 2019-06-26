/* global Dropzone */
/* global bootbox  */
Dropzone.options.drop = {
    paramName: "file", // The name that will be used to transfer the file
    maxFilesize: 24, // MB
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

function delete_syllabus(form_id) {
    swal({
        title: "Are you sure?",
        text: "You will not be able to recover this file!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false
    }, function() {
         $(form_id).submit();
    });
};


function showPrograms(division) {
     var programID = '#programs-'+ division;
    if($(programID).css('display') == 'none'){
        $(programID).css('display', 'block');   
       
    } else {
        $(programID).css('display', 'none');
       
    }

    $('#icon-'+ division).toggleClass('fa arrow')
    $('#icon-'+ division).toggleClass('fa arrow')
}


//$(document).ready(function() {
//  $("#side-menu li a").on('click', function(e) {
//        e.preventDefault();
//        var showMe = $(this)).data('showMe');
//        $("#coursesIcon-{{program.PID}} .showMe:not('.hide')").stop()
//        
//        function () {
//          $(this).addClass('hide');
//          $('#coursesIcon-{{program.PID}} .showMe[data-showMe="' +showMe+ '"]').removeClass('hide');
//        
//        }
//  
//  }
//
//}

var currentProg = null;
function showCourses(seid, program) {
  //coursesIcon-{{program.PID}}
  if (currentProg == null){  

    var programID = '#courses-'+ program;
    currentProg = '#coursesIcon-'+ program;
    console.log("the ID is" + programID);
    console.log("the current is" + currentProg);
    

        if($(programID).css('display') == 'none') {
        $(programID).css('display', 'block');
        
        
    } else {
        $(programID).css('display', 'none');
        //$('.coursesIcon-'+ program).hide();
    }
    
  for (prog in programID) {
  
    $(currentProg).toggleClass('fa arrow');
    $(currentProg).toggleClass('fa arrow')
    currentProg != null;
  } 
 }
}

function showAll() {
  $('.side-menu').metisMenu({ toggle: false });
  }

  $('.first-level').on('click', function(){
     $(this).children().toggleClass('fa arrow');
     $(this).children().toggleClass('fa arrow');
  });

 function showCourseTables (seid, pid){
   $.ajax({
     url: '/courses/showCourses/'+seid + "/" + pid,
     dataType: 'json',
     type: "GET",
     success: function (response){

     }
   })
}
