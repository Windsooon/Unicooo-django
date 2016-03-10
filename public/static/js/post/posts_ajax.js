var ajax_state = false;
$(document).on('show.bs.modal', '.modal', function () {
    var zIndex = 1040 + (10 * $('.modal:visible').length);
    $(this).css('z-index', zIndex);
    setTimeout(function() {
        $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
    }, 0);
});

$(document).ready(function(){
    var httpsUrl = "https://o3e6g3hdp.qnssl.com/";
    var page = 1
    var scrollTimeout;
    $activity_input = $(".activity-details-content input");
    var act_id = $activity_input.eq(0).val();
    var data = {"act_id": act_id, "page": page};
    var $container = $('#posts-container').masonry({
        columnWidth: 20,
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
        if (checkScroll($("#posts-container"), $(".post-container:last")) && ajax_state) {
            data.page += 1;
            ajax_state = false;
            get_post_list(data, $container);
        }
    };
    $("#post-details").on("show.bs.modal", function(e) {
        var post_id = $(e.relatedTarget).data('post-id');
        var reply_id = $("#user-id").val();
        var page = 1;
        var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        ajax_comment_list(reply_id, page)
        getPost(post_id, e);
        $("#really-delete-btn").on("click", function() {
            $.ajax({
                url: "/api/posts/" + post_id + "/",
                method: "DELETE",
                datatype: "json",
                beforeSend:function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                        xhr.setRequestHeader("X-CSRFToken", csrf_token);
                    } 
                },
                success: function() {
                  $container.masonry("remove", $("#post-" + post_id)).masonry('layout'); 
                  $('#post-details').modal('hide')
                  $('#post-delete-modal').modal('hide')
                },
            });
        });
    });

    $('#post-details').on('hidden.bs.modal', function (e) {
        $('audio').each(function(){
            this.pause(); // Stop playing
            this.currentTime = 0; // Reset time
        }); 
    })
   
    $("#add-comment-btn").on("click", comment_click_handler);
   
    $("#post-details").on("show.bs.modal", function(e) {
        
    });
})





