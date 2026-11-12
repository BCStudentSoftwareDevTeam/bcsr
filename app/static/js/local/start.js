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

$('#newDeadlineDescription, .deadlineEditTextarea').on('input', function() {
    autoResize(this);
});

(function () {
    var dateInput = document.getElementById('newDeadlineDate');
    var dateError = document.getElementById('newDeadlineDateError');
    if (!dateInput || !dateError) {
        return;
    }
    var dateGroup = dateInput.parentElement;

    function displayDateError() {
        var invalid = !dateInput.validity.valid;
        dateError.textContent = invalid
            ? 'Please enter a valid date with a year between 0001 and 9999.'
            : '';
        dateError.hidden = !invalid;
        dateInput.setAttribute('aria-invalid', invalid ? 'true' : 'false');
        dateGroup.classList.toggle('has-error', invalid);
    }

    dateInput.addEventListener('invalid', function (event) {
        event.preventDefault();
        displayDateError();
        dateInput.focus();
    });
    dateInput.addEventListener('blur', displayDateError);
    dateInput.addEventListener('change', displayDateError);
    dateInput.addEventListener('input', function () {
        if (dateInput.getAttribute('aria-invalid') === 'true') {
            displayDateError();
        }
    });
}());
