$('.ui.dropdown')
	.dropdown()
;

$('.tabular.menu .item').tab();


$(function(){
    (function ajax_get(){
        setTimeout(function(){
            $.ajax({
                type: 'POST',
                url: onlineURL,
                data: {
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken').val(),
                    'pk': $("input#online").val()
                },
                success: function(data){
                    ajax_get();
                }
            });
        }, 30000);
    })();
})