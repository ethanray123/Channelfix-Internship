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
    $('.tags').dropdown({
        onChange: function() {
            // console.log($(this).find("input").attr("id"));]
            $.ajax({
                type: "GET",
                url: window.location.pathname +'/tags',
                data: {
                    'stream_id': $(this).find("input").attr("id"),
                    'tag': $(this).find("input").attr("value")
                },
                success: function(data_receive){
                    console.log("success");
                }
            });
        }
    });
});
