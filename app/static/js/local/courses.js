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
  var elementIsClicked = false;
  function clickHandler() {
    elementIsClicked = true;
  }
  var isClicked = document.getElementById(programID);


  console.log('Here is the ' + programID + division)
  console.log('Here is the ' + programID + division)

  if (isClicked.addEventListener('click', clickHandler) == true) {
    if($(programID).css('display') == 'none'){
        $(programID).css('display', 'block');

    } else {
        $(programID).css('display', 'none');
    }


     $('#icon-'+ division).toggleClass('fa arrow')
     $('#icon-'+ division).toggleClass('fa arrow')
   }
  }




/*  $("ul.nav-tabs a").click(function (e) {
   e.preventDefault();
   $(this).tab('show');
 }); */

//}

/*
$(document).ready(function(){
  $('ul.nav-second-level').each(function(){
    var sideEl= $(this);
    $("a.{{program.name}}", sideEl).click(function(e){
    var programID= '#courses-'+ e;
    programID.preventDefault();
      sideEl2 = $("a.sideTab", sideEl);
      sideEl2.toggleClass();
      $("div.courses-{{program.PID}}").not(sideEl2).css('display', 'none');
      return false
  });
});
  $('html').click(function(){
    $("div.courses-{{program.PID}}").css('display', 'none')
  });
});

*/



function showCourses(seid, program) {
  //coursesIcon-{{program.PID}}
    var programID = '#courses-'+ program;
    console.log("the ID is" + programID);


    if ($(programID).css('display') == 'none') {
        $(programID).css('display', 'block');

    } else {
        $(programID).css('display', 'none');
        //$('.coursesIcon-'+ program).hide();
    }
    $('#coursesIcon-'+ program).toggleClass('fa arrow');
    $('#coursesIcon-'+ program).toggleClass('fa arrow');
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
