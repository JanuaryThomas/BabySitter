$(document).ready(function () {
    console.log("Hello........")
    $('.form-control-label').addClass("c-field__label");
    $('input[type=text], input[type=password], input[type=file], input[type=date]').addClass('c-input')
    $('input[type=submit]').addClass('c-btn c-btn--fullwidth c-btn--info');
    $('select').addClass('c-select__input');
    $('.form-group').addClass('c-field');


    $('#set-location').click(function () {
        var lat, lng;
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                lat = position.coords.latitude;
                lng = position.coords.longitude;

                data = {"lat": lat, "lng": lng};
                console.log(data);
                $('#alert-baby p').text("Loading..").show()
                $.ajax({
                    type: "POST",
                    contentType: 'application/json',
                    url: "https://baby-sitters.herokuapp.com/babysitter/set-location",
                    dataType: 'json',
                    data: JSON.stringify(data, null, "\t"),
                    success: function (data) {
                        console.log("Success......................")
                        console.log(data)
                    },


                });
            })
        }

    });


});