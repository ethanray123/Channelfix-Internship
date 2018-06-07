$(function(){
    $('#favorite').click(function(){
        if($(this).data('rating') == '1'){
            favorite('unfavorite')
            $(this).data('rating', '0')
        }
        else if($(this).data('rating') == '0'){
            favorite('favorite')
            $(this).data('rating', '1')
        }
    });

    function favorite(type){
        $.ajax({
            type: 'post',
            url: window.location.pathname + '/favorite',
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken').val(),
                type: type
            },
            success: function(response){
                console.log(response);
            }
        });
    }
})