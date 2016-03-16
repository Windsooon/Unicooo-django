$(document).ready(function(){
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
   
});

