$(document).ready(function(){
    $("#post-upload").on("show.bs.modal", function(e) {
        post_upload_status = false;
        if ($(".progress-bar").length == 0){
            $(".progress").append("<div class='progress-bar'></div>");
        }
    });

    var originalModal = $("#post-upload > .modal-dialog > .modal-content").clone();
    $("#post-upload").on('hidden.bs.modal', function(e) { 
        $("#post-upload > .modal-dialog").empty();
        var clone = originalModal.clone();
        $("#post-upload > .modal-dialog").append(clone);
        $(".progress-bar").remove();
    });

    $("#post-details").on("show.bs.modal", function(e) {
        var post_id = $(e.relatedTarget).data('post-id');
        var reply_id = $("#user-id").val();
        var page = 1;
        if ($(".request-user").text() == $(e.relatedTarget).parent().find(".post-user").text()) {
            getPost(post_id, e, true);
            delete_post(post_id);
        }
        else {
            getPost(post_id, e, false);
        }
        ajax_comment_list(reply_id, page)
    });

    $('#post-details').on('hidden.bs.modal', function (e) {
        $('audio').each(function(){
            this.pause();
            this.currentTime = 0;
        }); 
    })

    //like button animation
    $(".post-like-details-a").on("click", function(e) {
        var like_status = true;
        var post_id = $("#input-post-id").val();
        var post_author_id = $("#input-post-author-id").val();
        var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        if ($(".post-like-details-a").hasClass("glyphicon-heart-empty") && like_status == true) {
            like_status = false;
            $(".post-like-details-a").removeClass("glyphicon-heart-empty"); 
            $(".post-like-details-a").addClass("glyphicon-heart"); 
            $.ajax({
                    url: "/likes/" + post_id + "/",
                    method: "POST",
                    datatype: "json",
                    data: {"post_author_id": post_author_id},
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
                                alert("It seems a little problem with our server, Sorry for that, we will fix it soon.");
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

function delete_post(post_id) {
    $('#really-delete-btn').unbind().click(function() {
        var $container = $('.posts-container').masonry();
        var csrf_token = getCookie('csrftoken');
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
            error: function() {
                alert("You don't have permission to delete this post"); 
            },
        });
    });
}
