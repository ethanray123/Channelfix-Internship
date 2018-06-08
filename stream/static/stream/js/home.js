$("#filterCategory").change(function(){
	// get category
	var cat = $("#filterCategory").attr("value");
	// query lobbies with category
	$.ajax({
    type: 'GET',
    url: 'stream/lobbies/',
    data: {
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken').val(),
        'category_pk': cat
    },
    success: function(response){
      if(response == 0){
        $("#lobby-list").children(".ui.items").html("<h1>We've Come Up Empty</h1>");
      }else{
        window.location = '/?category_pk=' + cat;
      }
    }
  });
});
