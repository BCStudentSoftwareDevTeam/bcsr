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


function showCourses(seid, program) {
    var programID = '#courses-'+ program;
    if($(programID).css('display') == 'none'){
        $(programID).css('display', 'block');


    } else {
        $(programID).css('display', 'none');
    }

    $('#coursesIcon-'+ program).toggleClass('fa arrow')
    $('#coursesIcon-'+ program).toggleClass('fa arrow')
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
