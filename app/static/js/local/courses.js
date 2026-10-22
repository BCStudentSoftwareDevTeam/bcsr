/* global Dropzone */
/* global bootbox  */
Dropzone.autoDiscover = false;

$(function() {
    $(".syllabus-upload").each(function() {
        var form = this;
        var container = $(form).parent();
        var uploadButton = container.find(".syllabus-upload-button");
        var message = container.find(".syllabus-upload-message");
        var dropzone = new Dropzone(form, {
            paramName: "file",
            maxFilesize: 24, // MB
            maxFiles: 1,
            acceptedFiles: ".doc,.docx,.pdf,.txt,.zip",
            dictDefaultMessage: "Upload your syllabus here (one file)",
            dictMaxFilesExceeded: "Only one syllabus file is allowed. Remove the selected file before choosing another.",
            uploadMultiple: false,
            autoProcessQueue: false,
            addRemoveLinks: true,
            clickable: true,
            init: function() {
                var uploader = this;

                function updateUploadButton() {
                    uploadButton.prop("disabled", uploader.getQueuedFiles().length !== 1 ||
                        uploader.getUploadingFiles().length > 0);
                }

                uploader.on("addedfile", function() {
                    message.text("");
                });
                uploader.on("addedfiles", updateUploadButton);
                uploader.on("removedfile", function() {
                    message.text("");
                    updateUploadButton();
                });
                uploader.on("processing", function() {
                    uploadButton.prop("disabled", true);
                    message.text("Uploading syllabus...");
                });
                uploader.on("error", function(file, error, xhr) {
                    uploader.removeFile(file);
                    message.text(xhr ? "Upload failed. Please select the file and try again." : error);
                });
                uploader.on("success", function(file) {
                    $(file.previewElement).find(".dz-remove").remove();
                    uploader.disable();
                    uploadButton.prop("disabled", true);
                    message.text("Syllabus uploaded. Refresh the page to view the updated course.");
                });
            }
        });

        uploadButton.on("click", function() {
            if (dropzone.getQueuedFiles().length === 1 &&
                    dropzone.getUploadingFiles().length === 0) {
                dropzone.processQueue();
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
