$("button#subscribe").click(function(){
    var subscribe = $(this);
    $.ajax({
        type: 'POST',
        url: 'subscribe/',
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken').val(),
            'streamer_id': subscribe.attr("name")
        },
        success: function(response){
            console.log(response);
            if(response){
                subscribe.text("Unfollow");
            }else{
                subscribe.text("Follow");
            }
        }
    });
});