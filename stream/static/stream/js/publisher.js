$(function(){
    window.onbeforeunload = function() {
        return 'Your stream will be terminated';
    }
    var apiKey = "46119842";
    var session_id = $("#publisher").data("session_id");
    var pub_token = $("#publisher").data("pub_token");

    function handleError(error) {
      if (error) {
        console(error.message);
      }
    }

    var session = OT.initSession(apiKey, session_id);
    var publisher = null;
    var offlineBtn = $("button#offlineBtn");
    var goliveBtn = $("button#goliveBtn");
    session.connect(pub_token, function(error) {
        if (error) {
            handleError(error);
        }
        else{
            goliveBtn.removeClass('disabled');
            publisher = OT.initPublisher('publisher', {
                insertMode: 'append',
                width: '100%',
                height: '100%'
            }, handleError);
            session.publish(publisher, handleError);
            publisher.publishVideo(false);
            publisher.publishAudio(false);
            offlineBtn.click(function(){
                if (publisher) {
                    publisher.publishVideo(false);
                    publisher.publishAudio(false);
                    offlineBtn.addClass('disabled');
                    goliveBtn.removeClass('disabled');
                }
            });
            goliveBtn.click(function(){
                if (publisher) {
                    publisher.publishVideo(true);
                    publisher.publishAudio(true);
                    offlineBtn.removeClass('disabled');
                    goliveBtn.addClass('disabled');
                }
            });
        }
    });
});