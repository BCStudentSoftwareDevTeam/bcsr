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

var cid = 0;
$('input[type=checkbox]').change(function () {
    cid = $(this).data("cid");
    //Ensures state of None Required and all the other checkboxes can't be in an impossible state
    if($(this).prop('name') == "NoneRequired" && $(this).prop("checked")) {
        console.log("Clicked none required");
        var courseCheckboxes = $("td#" +cid).find("input:checkbox");
        console.log(courseCheckboxes);
        var first = true;
        $(courseCheckboxes).each(function() {
            console.log($(this));
            $(this).prop('checked', first);
            if (first) {
                first = false;
            }
        });
    } else if ($(this).prop("checked")) {
        $("td#" +cid).find("input:checkbox#NoneRequired").prop("checked", false);
    }

    //Submits the form
    var rightForm = $("td#" +cid).find("form#courseMaterials");
    $.ajax({
        type: "POST",
        url: rightForm.attr('action'),
        data: rightForm.serialize(), // serializes the form's elements.
        success: function(data)
            {
            }
    });
});

$('form#courseMaterials').submit(function(e){
    e.preventDefault();
});