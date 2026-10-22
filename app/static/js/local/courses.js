/* global Dropzone */
/* global bootbox  */
Dropzone.autoDiscover = false;

$(function() {
    $(".syllabus-upload").each(function() {
        var form = this;
        var container = $(form).parent();
        var submitButton = container.find(".syllabus-submit");
        var message = container.find(".syllabus-upload-message");
        var uploader = new Dropzone(form, {
            paramName: "file",
            maxFilesize: 24, // MB
            maxFiles: 1,
            acceptedFiles: ".doc,.docx,.pdf,.txt, .zip",
            dictDefaultMessage: "Upload your syllabus here",
            uploadMultiple: false,
            autoProcessQueue: false,
            addRemoveLinks: true,
            clickable: true,
            init: function() {
                var dropzone = this;

                function updateSubmitButton() {
                    submitButton.prop("disabled", dropzone.getQueuedFiles().length !== 1 ||
                        dropzone.getUploadingFiles().length > 0);
                }

                dropzone.on("addedfiles", updateSubmitButton);
                dropzone.on("removedfile", updateSubmitButton);
                dropzone.on("processing", function() {
                    submitButton.prop("disabled", true);
                    message.text("Submitting syllabus...");
                });
                dropzone.on("error", function() {
                    message.text("Submission failed. Remove the file and select it again to retry. Refresh the page if the syllabus was already submitted.");
                    updateSubmitButton();
                });
                dropzone.on("success", function(file) {
                    $(file.previewElement).find(".dz-remove").remove();
                    dropzone.disable();
                    submitButton.prop("disabled", true);
                    message.text("Syllabus submitted. Refresh the page to view the updated course.");
                });
            }
        });

        submitButton.on("click", function() {
            if (uploader.getQueuedFiles().length === 1 &&
                    uploader.getUploadingFiles().length === 0) {
                uploader.processQueue();
            }
        });
        $(form).on("submit", function(event) {
            event.preventDefault();
        });
    });
});

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
