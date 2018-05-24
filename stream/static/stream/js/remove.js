$(function(){
    $(".removed").click(function() {
        var csrf_token = $("#csrf_token").val();
        console.log($(this).is(':checked'));
        $.ajax({
            type: "GET",
            url: window.location.pathname +'/remove',
            data: {"csrfmiddlewaretoken": csrf_token,
                'model': $(this).attr("name"),
                'value': $(this).is(':checked'), 
                'pk': $(this).attr("id")
            },
            success: function(data_receive){
                console.log("dsd");
            }
    });
        
    });
});
