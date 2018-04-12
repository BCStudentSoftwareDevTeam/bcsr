

/* global Dropzone */
/* global bootbox  */
Dropzone.autoDiscover = false;
 Dropzone.options.drop = {
     paramName: "file", // The name that will be used to transfer the file
     maxFilesize: 5, // MB
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
