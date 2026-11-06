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
    init: function() {
        this.on("addedfile", function(file) {
            if (!file.previewElement || !this.element.classList.contains("syllabus-upload")) {
                return;
            }
            var filename = file.previewElement.querySelector(".dz-filename");
            if (filename) {
                // Keep the full name in the DOM; truncation is visual only.
                filename.setAttribute("tabindex", "0");
                filename.setAttribute("title", file.name);
                filename.setAttribute("aria-label", "Filename: " + file.name);
            }
        });
    },
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

    $('#icon-'+ division).toggleClass('glyphicon-plus')
    $('#icon-'+ division).toggleClass('glyphicon-minus')
}


function showCourses(program) {
    var programID = '#courses-'+ program;
    if($(programID).css('display') == 'none'){
        $(programID).css('display', 'block');


    } else {
        $(programID).css('display', 'none');
    }

    $('#coursesIcon-'+ program).toggleClass('glyphicon-plus')
    $('#coursesIcon-'+ program).toggleClass('glyphicon-minus')
}
