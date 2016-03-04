var ajax_state = true;
$(document).ready(function(){
    var page = 1;
    var data = {"act_type": 0, "page": page};
    var scrollTimeout;
    var $container = $(".row").masonry({
        itemSelector: '.act-outer-container',
        transitionDuration: '0.3s',
        hiddenStyle: { opacity: 0 },
        visibleStyle: { opacity: 1 }
    });
    get_act_list(data, $container)
    //scroll load more
    $(window).scroll(function () {
        if (scrollTimeout) {
            clearTimeout(scrollTimeout);
            scrollTimeout = null;
        }
        scrollTimeout = setTimeout(scrollHandler, 50);
    });
    scrollHandler = function () {
        // Check your page position
        if (checkScroll($(".act-outer-container")) && ajax_state) {
            data.page += 1;
            ajax_state = false;
            get_act_list(data, $container)
        }
    };
});    


