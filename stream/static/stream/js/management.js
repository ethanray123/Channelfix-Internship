$(function(){
    var id;
    $(".remove").click(function() {
        if(confirm("Mark as removed/unremoved?")){
            $.ajax({
                type: "POST",
                url: window.location.pathname +'/remove',
                data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken').val(),
                    'model': $(this).attr("name"),
                    'value': $(this).is(':checked'),
                    'pk': $(this).attr("id")
                },
                success: function(data_receive){

                }
            });
        }
    });
    $('.dropdown.tags').dropdown({
        onChange: function() {
            if($("input#main").attr("value") &&
               $(this).find("input").attr("value") == '3'){
                id = $(this).find("input").attr("id");
                $(".modal.tags").find("div.dropdown.tags").remove();
                var dropdown = $("div.dropdown.tags#" + $("input#main").attr("value")).clone();
                dropdown.dropdown();
                dropdown.addClass("clone");
                dropdown.find(".menu .item[data-value=3]").remove();
                dropdown.find(".text").html("Guest");
                $(".modal.tags").find("span").html(dropdown.find("span").html());
                $(".modal.tags").find("div.header").after(dropdown);
                $(".modal.tags").modal("show");
            }
            else{
                $.ajax({
                    type: "POST",
                    url: window.location.pathname +'/tags',
                    data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken').val(),
                        'stream_id': $(this).find("input").attr("id"),
                        'tag': $(this).find("input").attr("value")
                    },
                    success: function(data_receive){}
                });
            }
        }
    });
    $(".modal.tags div#change").click(function(){
        $.ajax({
            type: "POST",
            url: window.location.pathname +'/tags',
            data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken').val(),
                'stream_id': id,
                'tag': $(".dropdown.tags").find("input").attr("value"),
                'changed_tag': $("div.dropdown.tags.clone").find("input").val()
            },
            success: function(data_receive){
                $(".modal.tags").modal('hide');
            }
        });
    });
    var i = 0;
    (function ajax_get(){
        setTimeout(function(){
            $.ajax({
                type: 'GET',
                url: window.location.pathname +'/tags',
                success: function(data){
                    $("input#main").val(data.main.id);
                    $.each(data.streams, function(i, stream){
                        var dropdown = $(".dropdown.tags#" + stream.id);
                        dropdown.find("input#" + stream.id).val(stream.tag);
                        dropdown.find("div.text").html(stream.tag_display);
                    });
                    ajax_get();
                }
            });
        }, 3000);
    })();
});
