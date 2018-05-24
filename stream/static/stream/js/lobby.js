$(function(){
    //comment function
    $("input#txtComment").attr("autocomplete", "Off");

    var ctr = 0;
    (function ajax_get(){
        setTimeout(function(){
            $.ajax({
                type: 'GET',
                url: window.location.pathname +'/comments/',
                success: function(data){
                    if(ctr != data.comments.length){
                        $("ul#ulComment").empty();
                        var comment_holder;
                        console.log(data)
                        $.each(data.comments, function(ctr, comment){
                            comment_holder = $('li.comment.template').clone();
                            comment_holder.removeClass("template");
                            comment_holder.removeAttr("hidden");
                            comment_holder.find("img.avatar").attr("src", "/media/" + comment.owner__profile__avatar);
                            comment_holder.find("span.username").html(comment.owner__username);
                            comment_holder.find("span.when").html(comment.when);
                            comment_holder.find("span.text").html(comment.text);
                            if($("input#user").val() == comment.owner__username){
                                console.log("dsdsd");
                                comment_holder.find("div#container").after("<span class='remove'> [remove] </span>");
                                comment_holder.find("span.remove").attr("id", comment.pk);
                                comment_holder.find("span.remove").click(function(event){remove_comment(event);});
                            }
                            else{
                                comment_holder.find("div#container").after("<span class='report' id='" + comment.pk +  "'> [report] </span>");
                                comment_holder.find("span.report").click(report_comment);
                            }
                            comment_holder.appendTo("ul#ulComment");
                        });
                    }
                    ctr = data.comments.length
                    ajax_get();
                }
            });
        }, 500);
    })();

    function report_comment(){
        $("span#error").html("");
        $('.ui.modal').attr("id", $(this).attr("id"))
        $('.ui.modal').modal('show')
    };

    $(".ui.button#ok").click(function(event){
        if($("input#reason").val()){
            ajax_post(event, type="report", text="", pk=$("div.ui.modal").attr("id"), reason=$("input#reason").val());
            $('.ui.modal').modal('hide')
        }
        else{
            $("span#error").html("State Your Reason");
        }
    });


    function ajax_post(event, type, text, pk, reason){
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: window.location.pathname +'/comments/',
            data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken').val(),
                'type': type,'txtComment': text,'pk': pk, 'reason': reason
            },
            success: function(data){
                console.log(data);
                $("input#txtComment").val("");
            }
        });
    }

    function remove_comment(event){
        ajax_post(event, type="remove", text="", pk=$(event.target).attr("id"), reason="");
    }

    $("button#btnComment").click(function(event){
        ajax_post(event, type="create", text=$("input#txtComment").val(), pk=0, reason="");
    });//end of comment function

});