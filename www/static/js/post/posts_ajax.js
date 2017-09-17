var ajax_state = false;
//use to set multi model and make it index properly

$(document).on('show.bs.modal', '.modal', function () {
    var zIndex = 1040 + (10 * $('.modal:visible').length);
    $(this).css('z-index', zIndex);
    setTimeout(function() {
        $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
    }, 0);
});

$(document).ready(function(){
    var page = 1
    var scrollTimeout;
    $activity_input = $(".activity-details-content input");
    var act_id = $activity_input.eq(0).val();
    var data = {"act_id": act_id, "page": page};
    var $container = $('.posts-container').masonry({
        columnWidth: 1,
        itemSelector: '.post-container',
        transitionDuration: '0.3s',
        hiddenStyle: { opacity: 0 },
        visibleStyle: { opacity: 1 }
    });
    get_post_list(data, $container);
    $(window).scroll(function () {
        if (scrollTimeout) {
            clearTimeout(scrollTimeout);
            scrollTimeout = null;
        }
        scrollTimeout = setTimeout(scrollHandler, 50);
    });
    scrollHandler = function () {
        // Check your page position
        if (checkScroll($(".posts-container"), $(".post-container:last")) && ajax_state) {
            data.page += 1;
            ajax_state = false;
            get_post_list(data, $container);
        }
    };
    $("#add-comment-btn").on("click", comment_click_handler);
})
