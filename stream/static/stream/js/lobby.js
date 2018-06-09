$(function(){
    //comment function
    $("input#txtComment").attr("autocomplete", "Off");

    var ctr = 0;
    var flag = false;
    (function ajax_get(){
        setTimeout(function(){
            $.ajax({
                type: 'GET',
                url: window.location.pathname +'/comments/',
                success: function(data){
                    if(ctr != data.comments.length || flag){
                        $("ul#ulComment").empty();
                        var comment_holder;
                        $.each(data.comments, function(ctr, comment){
                            comment_holder = $('li.comment.template').clone();
                            comment_holder.removeClass("template");
                            comment_holder.removeAttr("hidden");
                            comment_holder.find("img.avatar").attr("src", "/media/" + comment.owner__profile__avatar);
                            comment_holder.find("span.username").html(comment.owner__username);
                            comment_holder.find("span.when").html(comment.when);
                            comment_holder.find("span.text").html(comment.text);
                            if($("input#user").val() == comment.owner__username){
                                comment_holder.find("div#container").after("<span class='remove'> [remove] </span>");
                                comment_holder.find("span.remove").attr("id", comment.pk);
                                comment_holder.find("span.remove").click(function(event){remove_comment(event);});
                            }
                            else{
                                if(!comment.isreported){
                                    comment_holder.find("div#container").after("<button class='report negative ui button' id='" + comment.pk +  "'> report </button>");
                                    comment_holder.find("button.report").click(report_comment);
                                }
                                else{
                                    comment_holder.find("div#container").after("<span> reported </span>");
                                }
                            }
                            comment_holder.appendTo("ul#ulComment");
                        });
                        flag = false;
                    }
                    ctr = data.comments.length
                    ajax_get();
                }
            });
        }, 3000);
    })();

    function report_comment(){
        $("span#error").html("");
        $('.modal.report').attr("id", $(this).attr("id"))
        $('.modal.report').modal('show')
    };

    $(".ui.button#ok").click(function(event){
        if($("input#reason").val()){
            ajax_post(event, type="report", text="", pk=$("div.modal.report").attr("id"), reason=$("input#reason").val());
            $('.modal.report').modal('hide')
            flag = true;
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

    $("button#joinBtn").click(function(event){
        event.preventDefault();
        var $this = $(this)
        var privacy = $this.data("privacy");
        if(privacy == "Public"){
            window.location = $this.data("url");
        }
        else if(privacy == "Private"){
            if($this.attr("data-ismember")){
                window.location = $this.data("url");
            }
            else{
                $.ajax({
                    type: 'POST',
                    url: $this.data("url"),
                    data: {
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken').val()
                    },
                    success: function(response){
                        $('#requestModal').modal('show');
                        setTimeout(function(){
                            $('#requestModal').modal('hide');
                            $this.addClass("disabled");
                        }, 5000);
                    }
                });
            }
        }
    });

    var apiKey = "46119842";
    function handleError(error) {
      if (error) {
        alert(error.message);
      }
    }

    (function getImage(){
        setTimeout(function(){
            $.ajax({
                type: 'GET',
                url: '/stream/api/stream',
                data: {
                    'lobby__pk': $("input#lobby").data("lobby_id"),
                    'start': 0,
                    'end': 10
                },
                success: function(response){
                    d = new Date();
                    $.each(response, function(ctr, stream){
                        var session_id = stream.session_id;
                        if(session_id)
                            $('#img' + session_id).attr('src', stream.image + '?' + d.getTime());
                    });
                    getImage();
                }
            });
        }, 5000);
    })();

    var session = null;
    var my_div = $('div#my_stream');

    if(my_div){
        sub_token = my_div.find('div.my_stream').data('sub_token');
        session_id = my_div.find('div.my_stream').attr('id');
        var my_session = OT.initSession(apiKey, session_id);
        my_session.on('streamCreated', function(event) {
        my_div.find('div.my_stream').append('<div id="my-stream-opentok"></div>');
            subscriber = my_session.subscribe(event.stream, 'my-stream-opentok', {
                insertMode: 'replace',
                width: '100%',
                height: '100%'
            }, handleError);
            subscriber.subscribeToAudio(false);
        });

        my_session.on("streamDestroyed", function(event) {
            event.preventDefault();
            my_session.unsubsribe(event.stream);
        });
        my_session.connect(sub_token);
    }

    function showStream(session_id, sub_token){
        session = OT.initSession(apiKey, session_id);
        $('#current-stream').append('<div id="current-stream-opentok"></div>');
        session.on('streamCreated', function(event) {
            subscriber = session.subscribe(event.stream, 'current-stream-opentok', {
                insertMode: 'replace',
                width: '100%',
                height: '100%'
            }, handleError);
        });

        session.on("streamDestroyed", function(event) {
            event.preventDefault();
            session.unsubsribe(event.stream);
        });
        session.connect(sub_token);
    }
    var stream_details = $('.content-container.stream');

    $('.streams').click(function(){
        if(session)
            session.disconnect();
        $('#current-stream').empty();
        showStream($(this).attr('id'), $(this).data('sub_token'));
        $.ajax({
            type: 'GET',
            url: '/stream/get_stream',
            data: {
                'session_id': $(this).attr('id'),
            },
            success: function(response){
                console.log(response);
                console.log(response.description);
                stream_details.removeAttr('hidden');
                stream_details.find('#stream-title').html(response.title);
                stream_details.find('#stream-tag').html(response.tag);
                stream_details.find('.owner-avatar').attr('src', response.owner.avatar);
                stream_details.find('#stream-owner-username').html(response.owner.username);
                stream_details.find('#stream-owner-username').attr('href', response.owner.url);
                stream_details.find('#stream-description').html(response.description);
                stream_details.find('#subscribe').attr('name', response.owner.id);
                console.log(response.is_subscribed);
                if(response.is_subscribed)
                    stream_details.find('#subscribe').text("Unfollow")
                else
                    stream_details.find('#subscribe').text("Follow")
            }
        });
    });
});
