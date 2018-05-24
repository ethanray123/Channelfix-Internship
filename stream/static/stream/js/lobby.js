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
                                if(!comment.reported){
                                    comment_holder.find("div#container").after("<span class='report'> [report] </span>");
                                    comment_holder.find("span.report").attr("id", comment.pk);
                                    comment_holder.find("span.report").click(function(event){report_comment(event);});
                                }
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

    function ajax_post(event, type, text, pk){
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: window.location.pathname +'/comments/',
            data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken').val(),
                'type': type,'txtComment': text,'pk': pk
            },
            success: function(data){
                console.log(data);
                $("input#txtComment").val("");
            }
        });
    }

    function remove_comment(event){
        ajax_post(event, type="remove", text="", pk=$(event.target).attr("id"));
    }

    function report_comment(event){
        ajax_post(event, type="report", text="", pk=$(event.target).attr("id"));
    }

    $("button#btnComment").click(function(event){
        ajax_post(event, type="create", text=$("input#txtComment").val(), pk=0);
    });//end of comment function
});