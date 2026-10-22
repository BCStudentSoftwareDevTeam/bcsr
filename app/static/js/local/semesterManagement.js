$(function () {
    $(".semester-download").click(function () {
        const message = $("<span>Preparing your download...</span>");

        $(this).after(message);

        setTimeout(function () {
            message.remove();
        }, 5000);
    });
});
