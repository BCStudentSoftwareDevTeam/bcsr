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
            dictDefaultMessage: "Choose or drop one syllabus file here",
            dictRemoveFile: "Remove selection",
            dictMaxFilesExceeded: "Only one syllabus file is allowed. Remove the selected file before choosing another.",
            uploadMultiple: false,
            autoProcessQueue: false,
            addRemoveLinks: true,
            clickable: true,
            previewTemplate: '<div class="dz-preview dz-file-preview">' +
                '<div class="dz-details"><div class="dz-filename"><span data-dz-name></span></div>' +
                '<div class="dz-size" data-dz-size></div></div>' +
                '<div class="dz-progress"><span class="dz-upload" data-dz-uploadprogress></span></div>' +
                '</div>',
            init: function() {
                var uploader = this;
                var selectionError = "";

                function updateUploadButton() {
                    uploadButton.prop("disabled", uploader.getQueuedFiles().length !== 1 ||
                        uploader.getUploadingFiles().length > 0);
                }

                function updateSelection() {
                    var submitting = uploader.getUploadingFiles().length > 0;
                    var guidance = submitting ? "Submitting syllabus..." : uploader.getQueuedFiles().length === 1
                        ? "Selected — not submitted. You can remove or replace this file before submitting."
                        : "Choose one file, then select Submit syllabus.";
                    $(form).attr("aria-busy", submitting ? "true" : "false");
                    uploadButton.text(submitting ? "Submitting..." : "Submit syllabus");
                    message.text(selectionError ? selectionError + " " + guidance : guidance);
                    message.toggleClass("text-danger", !!selectionError);
                    updateUploadButton();
                }

                uploader.on("addedfile", function() {
                    selectionError = "";
                });
                uploader.on("addedfiles", updateSelection);
                uploader.on("removedfile", function() {
                    selectionError = "";
                    updateSelection();
                });
                uploader.on("processing", function() {
                    uploadButton.prop("disabled", true);
                    uploadButton.text("Submitting...");
                    $(form).attr("aria-busy", "true");
                    $(form).find(".dz-remove").hide();
                    message.removeClass("text-danger").text("Submitting syllabus...");
                });
                uploader.on("error", function(file, error, xhr) {
                    uploader.removeFile(file);
                    selectionError = xhr ? "Submission failed. Please select the file and try again." : error;
                    updateSelection();
                });
                uploader.on("success", function(file) {
                    $(file.previewElement).find(".dz-remove").remove();
                    uploader.disable();
                    uploadButton.prop("disabled", true);
                    uploadButton.text("Submitted");
                    $(form).attr("aria-busy", "false");
                    message.removeClass("text-danger").text("Syllabus submitted successfully. Refresh the page to view the updated course.");
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
