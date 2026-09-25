$(function() {

    $('#side-menu').metisMenu({ toggle: false });

    window.setTimeout(function() {
        document.querySelectorAll('.alert.alert-dismissible').forEach(function(alert) {
            alert.remove();
        });
    }, 5000);

});

// when one makes a deadline this is supposed to make the popup close automatically after 5 seconds.
// https://www.w3schools.com/jsref/met_win_settimeout.asp