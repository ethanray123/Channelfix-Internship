$(function(){
    $(".remove").click(function() {
        var csrf_token = $("#csrf_token").val();
        if(confirm("Mark as removed/unremoved?")){
            $.ajax({
                type: "GET",
                url: window.location.pathname +'/remove',
                data: {"csrfmiddlewaretoken": csrf_token,
                    'model': $(this).attr("name"),
                    'value': $(this).is(':checked'), 
                    'pk': $(this).attr("id")
                },
                success: function(data_receive){
                    
                }
            });
        }        
    });
});
