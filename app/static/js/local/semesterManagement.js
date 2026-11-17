document.addEventListener("DOMContentLoaded", function () {
    $(".semester-download").click(function () {
        const message = $("<span>Preparing your download...</span>");

        $(this).after(message);

        setTimeout(function () {
            message.remove();
        }, 5000);
    });
});

// Shows the admin which term they are about to create
$(function() {
  var banner = $('#creatingTermName');
  function updateBanner() {
    var term = $('#term option:selected');
    var year = $('#year').val();
    if (term.val() && year) {
      banner.text(term.text() + ' ' + year);
    } else {
      banner.text('Choose a term and year');
    }
  }
  $('#term, #year').on('change', updateBanner);
  updateBanner();
});
