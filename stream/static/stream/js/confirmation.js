$("button.confirmation").click(function(event){
	var form = $(this).parent();
    event.preventDefault();
    $('#confirmationModal').modal('show');
    $("div.ok").click(function(){
    	form.submit();
    });
});
