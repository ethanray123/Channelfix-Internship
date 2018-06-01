$(function(){
    $('.ui.search').search({
        searchOnFocus: false,
        apiSettings : {
            url : '/stream/api/search?text={query}'
        },
        type: 'category'
    });
});