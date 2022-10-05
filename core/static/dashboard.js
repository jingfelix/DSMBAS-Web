

$(function () {
    $('.file-input-trigger').on('click', function () {
        $('.file-input').trigger('click');
    });
});

function getmsg() {
    $.get(
        $SCRIPT_ROOT + '/u/msg',
        function (data) {
            if (data != 'None') {
                mdui.snackbar({
                    message: data,
                    onclick: function () {
                        location.reload();
                    }
                });
            }
        });
}

setInterval(getmsg, 7000);