var comment_click_handler = function(e) {
    var comment_text = $(".comment-form-text").val();
    var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    var httpsUrl = "https://o3e6g3hdp.qnssl.com/"
    var avatarStyle = "-avatarSetting"
    if (comment_text.length < 1) {
        return false;
    }
        $.ajax({
            url: "/api/comments/",
            type: "POST",
            datatype: "json",
            data:  {csrfmiddlewaretoken: csrf_token, "reply_id": $("#input-post-author-id").val(), "post": $("#input-post-id").val(), "comment_content": comment_text},
            beforeSend: function() {
                $(".comment-form-text").prop("disabled", true);
            },
            success: function(data) {
                if ($(".form-server-error-div").length) {
                    $(".form-server-error-div").remove();
                }
                if ($("#user-avatar").val() == "/") {
                    var comment_avatar = $("<div />", {
                        "class": "comment-avatar",
                    });
                    var comment_avatar_empty_div = $("<div />", {
                        "class": "comment-avatar-empty-div",
                    });
                    var comment_avatar_empty_p = $("<p />", {
                        "class": "comment-avatar-empty-p",
                        text: $(".request-user").text().toUpperCase().charAt(0),
                    });
                    
                    comment_avatar_empty_div.append(comment_avatar_empty_p);
                    comment_avatar.append(comment_avatar_empty_div);
                }
                else {
                    var comment_avatar_s = $("<img />", {
                          src: httpsUrl + $("#user-avatar").val() + avatarStyle,
                          "class": "comment-avatar-s",
                      });

                      var comment_avatar = $("<div />", {
                          "class": "comment-avatar",
                      });
                      comment_avatar.append(comment_avatar_s);
                 }

                      var comment_avatar_a = $("<a />", {
                          "class": "comment-avatar-a pull-left",
                      });
                      //comment user and content
                      var comment_username_a = $("<a />", {
                          href: $("#base-user-username").val(),
                          "class": "comment-username-a",
                      });

                      var comment_username_p = $("<p />", {
                          "class": "comment-username-p",
                          text: $(".request-user").text(),
                      });

                      var comment_username = $("<div />", {
                          "class": "comment-username",
                      });

                      var comment_posttime_p = $("<p />", {
                          "class": "comment-posttime-p",
                          text: "Just now",
                      });

                      var comment_posttime = $("<div />", {
                          "class": "comment-posttime"
                      });

                      var comment_header = $("<div />", {
                          "class": "comment-header"
                      });
                       
                      comment_avatar_a.append(comment_avatar);
                      //
                      comment_username_a.append(comment_username_p);
                      comment_username.append(comment_username_a);
                      comment_posttime.append(comment_posttime_p);
                      comment_header.append(comment_username);

                      var comment_content = $("<div />", {
                          "class": "comment-content"
                      });

                      var comment_content_p = $("<p />", {
                          "class": "comment-content-p",
                          text:  comment_text,
                      });

                      comment_content.append(comment_content_p);

                      var comment_all = $("<div />", {
                          "class": "comment-all"
                      });

                      comment_all.append(comment_header);
                      comment_all.append(comment_content);
                      comment_all.append(comment_posttime);

                       var list_group_item = $("<li />", {
                          "class": "list-group-item"
                      });

                      list_group_item.append(comment_avatar_a);
                      list_group_item.append(comment_all);
                      list_group_item.hide().appendTo(".list-group").fadeIn();
                      $(".comment-form-text").val("");
                      //$(".comment-form").fadeOut();
              },
              error: function(xhr, status, error) {
                  if (xhr.status >= 400 && xhr.status < 500) {
                      error_text = "Please check again your input.";
                  }
                  else {
                      error_text = "Please try again later";
                  }
                  if ($(".form-server-error-div").length) {
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
        if ($(".comment-form-text").val().length) {
            var currrent_length=$(".comment-form-text").val().length;  
            if (currrent_length >= 1 && currrent_length <= 140) {
                $comment_length.text(140-currrent_length);
                if ($('#add-comment-btn').is(":disabled")) {
                    $('#add-comment-btn').prop('disabled', false);
                }
            }
            else if (currrent_length >140) {
                $comment_length.text("beyond 140 char");
                $comment_length.css("color","#3f51b5");
                $('#add-comment-btn').prop('disabled', true);
            }
        }
        else {
            $comment_length.text(140);
        }
    }); 

//personal page comments
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
                    var comment_image_a = $("<a />", {
                        "class": "comment-image-a pull-left",
                        href:  "/" + value["comment_author"] + "/act_crate/",
                        });
                    //if user avatar is empty
                    if (value["comment_avatar"]) {

                        var httpsUrl = "https://o3e6g3hdp.qnssl.com/";
                        var avatarStyle = "-avatarSetting";
                        var comment_image_div = $("<div />", {
                            "class": "comment-image-div",
                            });
                        var comment_image = $("<img />", {
                            src: httpsUrl + value["comment_avatar"] + avatarStyle,
                            "class": "comment-image",
                            });
                        comment_image_div.append(comment_image);
                        comment_image_a.append(comment_image_div);
                    }
                    else {
                        var comment_empty_image_div = $("<div />", {
                            "class": "comment-empty-image-div",
                            });
                        var comment_empty_image_p = $("<p />", {
                            "class": "comment-empty-image-p",
                            text: value["comment_author"].toUpperCase().charAt(0),
                            });
                        comment_empty_image_div.append(comment_empty_image_p);
                        comment_image_a.append(comment_empty_image_div);
                    }
                    var comment_author = $("<div />", {
                        "class": "comment-author",
                        });
                    var comment_author_a = $("<a />", {
                        "class": "comment-author-a",
                        href:  "/" + value["comment_author"] + "/act_crate/",
                        });
                    var comment_author_p = $("<p />", {
                        "class": "comment-author-p",
                        text: value["comment_author"]
                        });
                    var comment_content = $("<div />", {
                        "class": "comment-content-list",
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
                    comment_author.append(comment_author_a); 
                    comment_author_a.append(comment_author_p); 
                    comment_content.append(comment_content_p); 
                    comment_time.append(comment_time_p); 
                    comment_outer_div.append(comment_image_a);
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
        complete: function(data) {
            complete_data = $.parseJSON(data.responseText); 
            if (complete_data.next) {
                ajax_state = true;
            }
        }
    }); 
}

