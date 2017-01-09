$('#temp_button').click(function () {
    $.get('/temp_refresh', function (data) {
        $('#temp_cur').html(data);
    });
});