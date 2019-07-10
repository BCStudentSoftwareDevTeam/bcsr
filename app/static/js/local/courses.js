/* global Dropzone */
/* global bootbox  */
var global = this;
var currentProgram = "0";
var currentDivision = "0";
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
  console.log('Here is the ' + programID + division)
    if($(programID).css('display') == 'none'){
        $(programID).css('display', 'block');

    } else {
        $(programID).css('display', 'none');
    }

     $('#icon-'+ division).toggleClass('fa arrow')
     $('#icon-'+ division).toggleClass('fa arrow')
   }




  function showCourses(seid, program) {
    //coursesIcon-{{program.PID}}
      // $('#coursesIcon-'+ program).hide();
      console.log(this.currentProgram)
      if (this.currentProgram != "0"){
          $(this.currentProgram).css('display', 'none');
      }
      var programID = '#courses-'+ program;
      console.log("the ID is" + programID);
    //  var $this = $(this).parent().find('span');

      if ($(programID).css('display') == 'none') {
          $(programID).css('display', 'block');

      } else {
          $(programID).css('display', 'none');
          //$('.coursesIcon-'+ program).hide();
      }
        $('#coursesIcon-'+ program).show();
        this.currentProgram = programID
       }



  function showAll() {
    //var programID = '#courses-'+ program;
    console.log("Hello")
    var division_DIDs = [1, 2, 3, 4, 5, 6, 12]
    var division_length = division_DIDs.length
    var firstPID = 11
    var lastPID = 40
    var program_PIDs = []
    while(firstPID <= lastPID){
      program_PIDs.push(firstPID++)
    }
    var length = program_PIDs.length

    if (this.currentProgram != "0"){
        $(this.currentProgram).css('display', 'none');
    }

    if (this.currentDivision != "0"){
        $(this.currentDivision).css('display', 'none');
    }

    for (var k = 0; k < division_length; k++) {
      showPrograms(division_DIDs[k])
    }

    for (var i = 0; i < length; i++) {
    if ($('#courses-' + program_PIDs[i]).css('display') == 'none') {
      $('#courses-' + program_PIDs[i]).css('display', 'block');

    } else {
      $('#courses-' + program_PIDs[i]).css('display', 'none');
      //$('.coursesIcon-'+ program).hide();
    }
    $('#coursesIcon-'+ program_PIDs[i]).show();
    this.currentProgram = program_PIDs[i]
  }

  }
