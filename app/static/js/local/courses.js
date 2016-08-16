/* global Dropzone */
/* global bootbox  */
Dropzone.options.drop = {
    paramName: "file", // The name that will be used to transfer the file
    maxFilesize: 5, // MB
    acceptedFiles: ".doc,.docx,.pdf",
    accept: function(file, done) {
        done();
        console.log("hello");
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