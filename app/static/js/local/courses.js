/* global Dropzone */
Dropzone.options.drop = {
  paramName: "file", // The name that will be used to transfer the file
  maxFilesize: 5, // MB
  acceptedFiles: ".doc,.docx,.pdf",
  accept: function(file, done) {
     done(); }
};