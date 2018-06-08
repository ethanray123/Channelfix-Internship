$('.ui.dropdown')
	.dropdown()
;

$('.tabular.menu .item').tab();


$(function(){
    (function ajax_get(){
        setTimeout(function(){
            $.ajax({
                type: 'POST',
                url: window.location.pathname +'/online',
                data: {
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken').val(),
                    'pk': $("input#online").val()
                },
                success: function(data){
                    ajax_get();
                }
            });
        }, 5000);
    })();
})