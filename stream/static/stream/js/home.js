$("#filterCategory").change(function(){
	// get category
	var cat = $("#filterCategory").attr("value");
	// query lobbies with category
	$.ajax({
    type: 'GET',
    url: 'stream/lobbies/',
    data: {
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken").val(),
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
var lobbyoffset = 10;
$("#loadmoreLobbies").click(function(){
  event.preventDefault();
  $.ajax({
    type: 'GET',
    url: 'stream/loadmore/',
    data: {
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken").val(),
        'offset': lobbyoffset,
        'loadtype': "lobbies"
    },
    success: function(response){
      console.log(response);
      if(response.length == 0){
        var endmessage = '<div class="ui horizontal divider">';
        endmessage = endmessage + 'No Lobbies at this time</div>'
        $("#lobby-list").children(".ui.items").append(endmessage);
        $('#loadmoreLobbies').hide();
      }else{
        for (var i = 0; i < response.length; i++) {
          var lobbies = '<div class="item lobby">';
          lobbies = lobbies+'<a class="image lobby-image" href="stream/lobby/'+response[i].id+'">';
          lobbies = lobbies+'<img src="'+response[i].image+'"></a>';
          lobbies = lobbies+'<div class="content">';
          lobbies = lobbies+'<div class="header title">';
          lobbies = lobbies+'<a href="stream/lobby/'+response[i].id+'">';
          lobbies = lobbies+response[i].name+'</a></div><br>'; // header title end
          lobbies = lobbies+'<div class="category">'+response[i].category+'</div>'
          lobbies = lobbies+'<div class="ui horizontal list">';
          lobbies = lobbies+'<div class="item">';
          lobbies = lobbies+'<img class="ui avatar image" src="'+response[i].owner.avatar+'">';
          lobbies = lobbies+'<div class="content">';
          lobbies = lobbies+'<div class="header">';
          lobbies = lobbies+'<a href="stream/profile/'+response[i].owner.profile_id+'">';
          lobbies = lobbies+response[i].owner.username+'</a></div>'; //header end
          lobbies = lobbies+'</div>'; //content end 
          lobbies = lobbies+'</div>'; //item end
          lobbies = lobbies+'</div>'; //ui horiz end
          lobbies = lobbies+'<div class="meta">'+response[i].when+'</div>';
          lobbies = lobbies+'<div class="description"><p>'+response[i].description+'</p>';
          lobbies = lobbies+'</div>'; //description end
          lobbies = lobbies+'<div class="ui two statistics">';
          lobbies = lobbies+'<div class="statistic">';
          lobbies = lobbies+'<div class="value">'+response[i].views+'</div>';
          lobbies = lobbies+'<div class="label">Views</div>';
          lobbies = lobbies+'</div>'; //statistic end
          lobbies = lobbies+'<div class="statistic">';
          lobbies = lobbies+'<div class="value">'+response[i].streams+'</div>';
          lobbies = lobbies+'<div class="label">Streams</div>';
          lobbies = lobbies+'</div>'; //statistic end
          lobbies = lobbies+'</div>'; //statistics end
          lobbies = lobbies+'</div>'; //lobby image end
          lobbies = lobbies+'</div>'; //item lobby end

          $("#lobby-list").children(".ui.items").append(lobbies);
        }
        
        lobbyoffset += 5;
        console.log("lobbyoffset: "+ lobbyoffset);
      }
    }
  });
});

var notificationoffset = 5;
$("#loadmoreNotifications").click(function(){
  event.preventDefault();
  $.ajax({
    type: 'GET',
    url: 'stream/loadmore/',
    data: {
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken").val(),
        'offset': notificationoffset,
        'loadtype': "notifications"
    },
    success: function(response){
      console.log(response);
      if(response.length == 0){
        $('#loadmoreNotifications').hide();
      }else{
        for (var i = 0; i < response.length; i++) {
          var notifications = '<div class="item"><i class="bell icon"></i>';
          notifications = notifications+'<div class="content">';
          notifications = notifications+'<a class="header" href="stream/'+response[i].redirect_to+response[i].redirect_id+'">';
          notifications = notifications+response[i].details+'</a></div>';

          $("#notification-list").children(".notifications").append(notifications);
        }
        
        notificationoffset += 5;
        console.log("notificationoffset: "+ notificationoffset);
      }
    }
  });
});

var useroffset = 10;
$("#loadmoreUsers").click(function(){
  event.preventDefault();
  $.ajax({
    type: 'GET',
    url: 'stream/loadmore/',
    data: {
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken").val(),
        'offset': useroffset,
        'loadtype': "users"
    },
    success: function(response){
      console.log(response);
      if(response.length == 0){
        $('#loadmoreUsers').hide();
      }else{
        for (var i = 0; i < response.length; i++) {
          var users = '<div class="item">';
          if (response[i].avatar) {
            users = users+'<img class="ui avatar image" src="'+response[i].avatar+'">';
          }else{
            users = users+'<img class="ui avatar image" src="/media/stream/static/images/default_avatar.png">';
          }
          users = users+'<div class="content">';
          users = users+'<a class="header" href="stream/profile/'+response[i].profile_id+'">';
          users = users+response[i].username+'</a></div>';
          users = users+'</div>';
          $("#user-list").children(".users").append(users);
        }
        
        useroffset += 5;
        console.log("notificationoffset: "+ useroffset);
      }
    }
  });
});
