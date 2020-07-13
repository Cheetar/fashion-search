$('#upload').change(function () {
    var files = $(this).prop('files');

    if (files && files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#uploadGroup').slideUp(500);
            $('#imageCard').slideDown(500);
            $('#imageResult').attr('src', e.target.result);
        };
        reader.readAsDataURL(files[0]);
    }
});

$('#cancelButton, #foundAgain').click(function() {
    $('#upload').val('');
    $('#uploadGroup').slideDown(500);
    $('#imageCard').slideUp(500);
    $('#imageCardContainer').removeClass('card-container-manualflip');
    $('#uploadConfirm').show();
    $('#uploadProgress').hide();
});

$('#searchButton').click(function() {
    $('#uploadConfirm').hide();
    $('#uploadProgress').show();

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
        $('#uploadConfirm').show();
        $('#uploadProgress').hide();
        $('.progress-bar').addClass('.progress-bar-animated');
        alert('Oops something went wrong.');
    });
});

$(".sliding-link").click(function(e) {
    e.preventDefault();
    var aid = $(this).attr("href");
    var top = aid === "#" ? 0 : $(aid).offset().top;
    $('html,body').animate({scrollTop: top}, 'slow');
});