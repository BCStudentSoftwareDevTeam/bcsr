$(function() {

    $('#side-menu').metisMenu({ toggle: false });

    window.setTimeout(function() {
        $('.alert.alert-dismissible').alert('close');
    }, 5000);

});