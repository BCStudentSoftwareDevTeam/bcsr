// Every HTML page should have a complimentary JS file, 
// even if it's empty
$('#editDeadline').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var id = button.data('id')
  var description = button.data('description')
  // Update the modal's content
  var modal = $(this)
  modal.find('#deadlineid').val(id)
  modal.find('#deadlineDescription').val(description) 
});

$('#editDeadline').on('shown.bs.modal', function() {
    var textarea = $(this).find('.deadlineEditTextarea')[0];

    if (textarea) {
        autoResize(textarea);
    }
});

$('#deleteDeadline').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var id = button.data('id') // Extract info from data-id
  var modal = $(this)
  modal.find('#deadlineid').val(id)
});

function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 300) + 'px';
}

$('#exampleTextarea, .deadlineEditTextarea').on('input', function() {
    autoResize(this);
});