$(function(){
    $('.ui.search').search({
        searchOnFocus: false,
        apiSettings : {
            url : '/stream/api/search?text={query}',
            method: 'GET',
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            onResponse: function(response){
                console.log(response);
                var convertedResponse = {
                    results : []
                };
                $.each(response.streams, function(index, item) {
                    convertedResponse.results.push({
                        category    : 'Stream',
                        title       : item.title,
                        description : item.tag,
                        image       : item.image
                    });
                });
                $.each(response.lobbies, function(index, item) {
                    convertedResponse.results.push({
                        category    : 'Lobby',
                        title       : item.name,
                        description : item.type,
                        image       : item.image
                    });
                });
                $.each(response.users, function(index, item) {
                    convertedResponse.results.push({
                        category    : 'User',
                        title       : item.username,
                        description : item.nickname,
                        image       : item.avatar
                    });
                });
                return convertedResponse;
            },
        },
    });
});