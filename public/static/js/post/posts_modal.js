$(document).ready(function(){
    var $container = $('#posts-container').masonry();
    $("#post-upload").on("hidden.bs.modal", function(e) {
        rebuild_modal($("#post-upload"));
    });

    $("#post-details").on("show.bs.modal", function(e) {
        var post_id = $(e.relatedTarget).data('post-id');
        var reply_id = $("#user-id").val();
        var page = 1;
        var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        ajax_comment_list(reply_id, page)
        getPost(post_id, e);
        $("#really-delete-btn").one("click", function() {
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

function rebuild_modal($modal) {
    $modal.html("");
    var csrftoken = getCookie('csrftoken');
    var elem = "<div class='modal-dialog'>" + 
                       "<div class='modal-content'>" + 
                           "<div class='modal-header'>" +
                               "<button type='button' class='close' data-dismiss='modal' aria-label='Close'>" + 
                                  "<span aria-hidden='true'>&times;</span></button>" +
                               "</button>" + 
                               "<h4 class='modal-title' class='inter-act-content'>Post Content</h4>" +
                           "</div>" +
                           "<div class='modal-body'>" +
                               "<div class='post-upload-wrapper'>" +
                                   "<div class='post-upload-div'>" +
                                       "<img class='post-upload-img' src=" + httpsUrl + "post-example.jpg" + ">" +
                                   "</div>" +
                                   "<div class='progress'>" +
                                       "<div class='progress-bar'></div>" +
                                   "</div>" +
                                   "<span class='upload-cover btn btn-primary btn-file btn-block'>" +
                                       "<span class='inter-upload-post'>Upload Image / Audio</span>" +
                                           "<input type='file' class='post-upload-image' accept='image/*, audio/* '>" +
                                   "</span>" +
                               "</div>" +
                               "<div class='post-form'>" +
                                   "<form method='POST' class='post-content'>" +
                                       "<input type='hidden' name='csrfmiddlewaretoken' value=" + csrftoken + ">" + 
                                       "<div class='form-group'>" +
                                           "<label class='sr-only' for='' >Post Content</label>" +
                                           "<input type='text' class='post-form-text form-control'  class='inter-upload-holder' placeholder='Please enter you post content.' disabled>" + 
                                           "<h6 class='post-form-length'>60</h6>" +
                                       "</div>" +
                                       "<button type='submit' disabled class='add-post-btn btn btn-primary pull-right'>Submit</button>" +
                                       "<button type='submit' disabled class='add-upload-more-btn btn btn-primary pull-right'>More</button>" +
                                   "</form>" +
                               "</div>" +
                           "</div>" +
                           "<div class='modal-footer'>" + 
                           "</div>" + 
                       "</div>" +
               "</div>";
    $modal.append(elem);
    $("#post-upload-change").on("hidden.bs.modal", function (e) {
        $(this).remove();
    });
}
