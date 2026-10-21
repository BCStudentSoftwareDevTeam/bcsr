$(function() {

    $('#side-menu').metisMenu({ toggle: false });

    window.setTimeout(function() {
    $('.flasher').fadeOut(600, function() {
        $(this).alert('close');
    });
}, 5000);

});
