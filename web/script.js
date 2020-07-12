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
    setTimeout(function() {
        $('#foundImage').attr('src', $('#imageResult').attr('src'));
        $('#imageCardContainer').addClass('card-container-manualflip');
    }, 3000);
});