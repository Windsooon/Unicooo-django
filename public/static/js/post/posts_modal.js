$(document).ready(function(){
    var $container = $('#posts-container').masonry();
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

    //like button animation
    $('.post-like-details-a').on('click', function(e) {
        var like_status = true;
        var post_id = $('#input-post-id').val();
        var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        if ($('.post-like-details-a').hasClass('glyphicon-heart-empty') && like_status == true) {
            like_status = false;
            $('.post-like-details-a').removeClass('glyphicon-heart-empty'); 
            $('.post-like-details-a').addClass('glyphicon-heart'); 
            $.ajax({
                    url: "/likes/" + post_id + "/",
                    method: "POST",
                    datatype: "json",
                    data: {"like": 1},
                    beforeSend:function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                            xhr.setRequestHeader("X-CSRFToken", csrf_token);
                        } 
                    },
                    error: function() {
                        setTimeout(
                            function() 
                            {
                                $('.post-like-details-a').removeClass('glyphicon-heart'); 
                                $('.post-like-details-a').addClass('glyphicon-heart-empty'); 
                                alert("Something run with our server, We will figure it out soon");
                            }, 3000);
                    },
                    success: function() {
                    },
                    complete: function() {
                        like_status = true; 
                    },
            });
        }
    });
   
});

