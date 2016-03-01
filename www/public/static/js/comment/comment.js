$(document).ready(function() {
    var reply_id = $("#user-id").val();
    var page = 1;
    ajax_comment_list(reply_id, page)
});

var comment_click_handler = function(e) {
    var comment_text = $(".comment-form-text").val();
        $.ajax({
            url: "/api/comments/",
            type: "POST",
            datatype: "json",
            data:  {csrfmiddlewaretoken: window.CSRF_TOKEN, "reply_id": e.data.user_id, "post": e.data.post_id, "comment_content": comment_text},
            beforeSend: function() {
                $(".comment-form-text").prop("disabled", true);
            },
            success: function(data) {
                if ($(".form-server-error-div").length) {
                    $(".form-server-error-div").remove();
                }
                var comment_avatar_s = $("<img />", {
                          src: $("#base-user-avatar").val(),
                          "class": "comment-avatar-s",
                      });

                      var comment_avatar = $("<div />", {
                          "class": "comment-avatar",
                      });
                      
                      var comment_avatar_a = $("<a />", {
                          "class": "comment-avatar-a pull-left",
                      });
                    
                      comment_avatar.append(comment_avatar_s);
                      comment_avatar_a.append(comment_avatar);

                      //comment user and content
                      var comment_username_a = $("<a />", {
                          href:  $("#base-user-username").val(),
                          "class": "comment-username-a",
                      });

                      var comment_username = $("<div />", {
                          "class": "comment-username",
                      });

                      var comment_posttime_span = $("<span />", {
                          text: "just now",
                      });

                      var comment_posttime = $("<div />", {
                          "class": "comment-posttime"
                      });

                      var comment_header = $("<div />", {
                          "class": "comment-header"
                      });
                        
                      comment_username.append(comment_username_a);
                      comment_posttime.append(comment_posttime_span);
                      comment_header.append(comment_username);
                      comment_header.append(comment_posttime);

                      var comment_content = $("<div />", {
                          "class": "comment-content"
                      });

                      var comment_content_p = $("<p />", {
                          text:  comment_text,
                      });

                      comment_content.append(comment_content_p);

                      var comment_all = $("<div />", {
                          "class": "comment-all"
                      });

                      comment_all.append(comment_header);
                      comment_all.append(comment_content);

                       var list_group_item = $("<li />", {
                          "class": "list-group-item"
                      });

                      list_group_item.append(comment_avatar_a);
                      list_group_item.append(comment_all);
                      list_group_item.hide().appendTo(".list-group").fadeIn();
                      $(".comment-form-text").val("");
              },
              error: function(xhr, status, error) {
                  if (xhr.status >= 400 && xhr.status < 500) {
                      error_text = "Please check again your input.";
                  }
                  else {
                      error_text = "Please try again later";
                  }
                  if ($(".form-server-error-div").length) {
                      console.log("already");    
                    } 
                  else {
                      $form_server_error_div = $("<div />", {"class": "form-server-error-div"});
                      $form_server_error_span = $("<span />", {"class": "pull-left form-server-error-span glyphicon glyphicon-exclamation-sign"});
                      $form_server_error_p = $("<p />", {"class": "form-server-error-p", text: error_text});
                      $form_server_error_span.appendTo($form_server_error_div).hide().fadeIn();
                      $form_server_error_p.appendTo($form_server_error_div).hide().fadeIn();
                      $form_server_error_div.appendTo($(".comment-form")).fadeIn(500);
                  }


              }, 
              complete: function(){
                $(".comment-form-text").prop("disabled", false);
            },
         });
    }

    //显示剩余输入字数
    $(".comment-form-text").keyup(function(){  
        var $comment_length = $(".comment-form-length");
        //length未必存在
        var currrent_length=$(".comment-form-text").val().length + 1;   
        if (currrent_length <= 140) {
            $comment_length.text(141-currrent_length);
        }
        else {
            $comment_length.text("beyond 140 char");
            $comment_length.css("color","#3f51b5");
        }
    }); 

function ajax_comment_list(reply_id, page){
    $.ajax({
        url: "/api/comments/",
        type: "GET",
        datatype: "json",
        data: {"reply_id": reply_id, "page": page},
        success: function(data) {
            if (data.results.length) {
                $.each(data.results, function(key, value){
                    var date = value["comment_create_time"].split("T", 1);
                    var comment_outer_div = $("<div />", {
                        "class": "comment-outer-div",
                        });
                    var comment_image_div = $("<div />", {
                        "class": "comment-image-div",
                        });
                    var comment_image = $("<img />", {
                        src: value["comment_avatar"],
                        "class": "comment-image",
                        });
                    var comment_author = $("<div />", {
                        "class": "comment-author",
                        });
                    var comment_author_p = $("<p />", {
                        "class": "comment-author-p",
                        text: value["comment_author"]
                        });
                    var comment_content = $("<div />", {
                        "class": "comment-content",
                        });
                    var comment_content_p = $("<p />", {
                        "class": "comment-content-p",
                        text: value["comment_content"]
                        });
                    var comment_time = $("<div />", {
                        "class": "comment-time",
                        });
                    var comment_time_p = $("<p />", {
                        "class": "comment-time-p",
                        text: date,
                        });
                    comment_image_div.append(comment_image);
                    comment_author.append(comment_author_p); 
                    comment_content.append(comment_content_p); 
                    comment_time.append(comment_time_p); 
                    comment_outer_div.append(comment_image_div);
                    comment_outer_div.append(comment_author);
                    comment_outer_div.append(comment_content);
                    comment_outer_div.append(comment_time);
                    comment_outer_div.append('<hr />');
                    $(".comment-wrapper").append(comment_outer_div);
                });
            }
            else {
                var empty_comment = $("<div />", {
                        "class": "empty-comment",
                        });
                var empty_comment_p = $("<p />", {
                        "class": "empty-comment-p",
                        text: "Nothing yet."
                        });
                empty_comment.append(empty_comment_p);
                empty_comment.appendTo($(".comment-wrapper")).hide().fadeIn();
            }
        },
    }); 
}
