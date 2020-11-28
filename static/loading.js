$("#scriptCall").click( function()
    {
        // when a button is clicked, you make an Ajax call.
        $('#loadingImage').show();
        $.ajax({
            type: "GET",
            url: '/results',
            success: function (resp) {
                $('#loadingImage').hide();
             }
        });
    });