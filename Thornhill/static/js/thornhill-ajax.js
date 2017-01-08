$('#temp_button').click(function () {
    $.get('/temp_refresh', function (data) {
        console.log(data);
        $('#temp_cur').html(data);
    });
});