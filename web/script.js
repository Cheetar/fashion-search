$('#upload').change(function () {
    var files = $(this).prop('files');

    if (files && files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#uploadGroup').css('display', 'none');
            $('#imageCard').css('display', 'block');
            $('#imageResult').attr('src', e.target.result);
        };
        reader.readAsDataURL(files[0]);
    }
});

$('#cancelButton, #foundAgain').click(function() {
    $('#upload').val('');
    $('#uploadGroup').css('display', '');
    $('#imageCard').css('display', 'none');
    $('#imageCardContainer').removeClass('card-container-manualflip');
    $('#uploadConfirm').css('display', '');
    $('#uploadProgress').css('display', 'none');
});

$('#searchButton').click(function() {
    $('#uploadConfirm').css('display', 'none');
    $('#uploadProgress').css('display', '');

    $('.progress-bar').width('100%');
    $('.progress-bar').addClass('.progress-bar-animated');

    var formData = new FormData($('#form')[0]);
    formData.append('file', $('input[name=file]')[0].files[0]); // wtf?

    $.ajax({
        url: "/",
        type: 'POST',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        uploadProgress: function(evt) {
            if (evt.lengthComputable) {
                var percentComplete = evt.loaded / evt.total;
                var percentValue = percentComplete + '%';
                $("#progressBar").animate({
                    width: percentValue
                }, {
                    duration: 500,
                    easing: "linear"
                });
                if (percentComplete == 100)
                    $('.progress-bar').addClass('.progress-bar-animated');
                else
                    $('.progress-bar').removeClass('.progress-bar-animated');
            } else {
                $('.progress-bar').addClass('.progress-bar-animated');
            }
        }
    }).done(function(data) {
        $('#foundImage').attr('src', data.found_image);
        $('#foundBuy').attr('href', data.url);
        $('#foundPrice').text(data.price);
        $('#imageCardContainer').addClass('card-container-manualflip');
    }).fail(function() {
        $('#uploadConfirm').css('display', '');
        $('#uploadProgress').css('display', 'none');
        $('.progress-bar').addClass('.progress-bar-animated');
        alert('Oops something went wrong.');
    });
});