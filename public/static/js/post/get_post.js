function getPost(post_id, e) {
        return $.ajax({
            url: "/api/posts/" + post_id + "/",
            type: "GET",
            datatype: "json",
            beforeSend: function(){
            },
            success: function(data) {
              if (data) {
                  var httpsUrl = "https://o3e6g3hdp.qnssl.com/";
                  var avatarStyle = "-avatarSetting";
                  var imageStyle = "-postDetails";
                  var post_image_b = $(".post-image-b");
                  if ($("#user-id").val() == data["post_user"]["id"]) {
                     $("#post-delete").css("display", "block");
                  }
                  if (data["post_mime_types"] == 0) {
                      post_image_b.empty(); 
                      var post_thumb_url = httpsUrl + data["post_thumb_url"] + imageStyle;
                      var post_raw_details = $("<img />", {
                          "class": "post-raw-details",
                          src: post_thumb_url,
                      });
                      post_image_b.append(post_raw_details);
                  }
                  else if (data["post_mime_types"] == 1) {
                      post_image_b.empty(); 
                      var audio_div_warpper = $("<div />", {
                          "class": "audio-div-wrapper",
                      });
                      var audio_div= $("<div />", {
                          "class": "audio-div",
                      });
                      var audio_fadeout= $("<div />", {
                          "class": "act-fadeout",
                      });
                      var audio_div_audio= $("<audio />", {
                          "class": "audio-div-audio",
                          src: httpsUrl + data["post_thumb_url"],
                          "controls": "controls",
                          "preload": "auto"
                      });
                      if (data["post_content"].length <= 10) {
                          var audio_div_p= $("<p />", {
                              "class": "audio-div-p",
                              text: data["post_content"]
                          });
                      }
                      else {
                         var audio_div_p= $("<p />", {
                             "class": "audio-div-p-small",
                             text: data["post_content"]
                         });
                      }
                      audio_div.append(audio_div_p);
                      audio_div_warpper.append(audio_div);
                      post_image_b.append(audio_div_warpper);
                      post_image_b.append(audio_fadeout);
                      post_image_b.append(audio_div_audio);
                  }
                  var elems = [];
                  var post_date = data["post_create_time"].split("T", 1);
                  $(".list-group").empty();
                  $(e.currentTarget).find(".post-raw-details").attr("src",post_thumb_url);
                  $("#input-post-id").val(post_id);
                  $("#input-post-author-id").val(data["user"]);
                  $(".post-details-a").attr("href", "/" + data["post_user"]["user_name"] + "/act_create")
                  $(".post-details-user").text(data["post_user"]["user_name"]);
                  $(".post-details-posttime").text(post_date);
                  $(".post-details-content-p").text(data["post_content"]);
                  $.each(data["post_comment"], function(key, value){
                      //comment avatar
                      var date = value["comment_create_time"].split("T", 1);
                      var comment_avatar = $("<div />", {
                          "class": "comment-avatar",
                      });
                      // if user avater is empty
                      if (value["comment_user"]["user_avatar"]) {
                          var comment_avatar_s = $("<img />", {
                              src: httpsUrl + value["comment_user"]["user_avatar"] + avatarStyle ,
                              "class": "comment-avatar-s",
                          });

                          comment_avatar.append(comment_avatar_s);
                      }
                      else {
                          var comment_avatar_empty_div = $("<div />", {
                              "class": "comment-avatar-empty-div",
                          });
                          var comment_avatar_empty_p = $("<p />", {
                              "class": "comment-avatar-empty-p",
                              text: value["comment_user"]["user_name"].toUpperCase().charAt(0),
                          });

                          comment_avatar_empty_div.append(comment_avatar_empty_p);
                          comment_avatar.append(comment_avatar_empty_div);
                      }

                      
                      var comment_avatar_a = $("<a />", {
                          "class": "comment-avatar-a pull-left",
                          href:  "/" + value["comment_user"]["user_name"] + "/act_crate/",
                      });
                    
                      comment_avatar_a.append(comment_avatar);

                      //comment user and content
                      var comment_username_a = $("<a />", {
                          href:  "/" + value["comment_user"]["user_name"] + "/act_crate/",
                          "class": "comment-username-a",
                      });
                        
                      var comment_username_p = $("<p />", {
                          "class": "comment-username-p",
                          text: value["comment_user"]["user_name"],
                      });

                      var comment_username = $("<div />", {
                          "class": "comment-username",
                      });

                      var comment_posttime_p = $("<p />", {
                          "class": "comment-posttime-p",
                          text: date,
                      });

                      var comment_posttime = $("<div />", {
                          "class": "comment-posttime"
                      });

                      var comment_header = $("<div />", {
                          "class": "comment-header"
                      });
                        
                      comment_username_a.append(comment_username_p);
                      comment_username.append(comment_username_a);
                      comment_posttime.append(comment_posttime_p);
                      comment_header.append(comment_username);

                      var comment_content = $("<div />", {
                          "class": "comment-content"
                      });

                      var comment_content_p = $("<p />", {
                          "class": "comment-content-p",
                          text:  value["comment_content"],
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
                      
                      $(".list-group").append(list_group_item);
                  });
              }
            },
            complete:function(){
            }
        });
    }
