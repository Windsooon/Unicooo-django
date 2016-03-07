var ajax_state = false;
$(document).ready(function(){
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
        ajax_comment_list(reply_id, page)
        getPost(post_id, e);
    });
    
    $("#add-comment-btn").on("click", comment_click_handler);
            
    
    function getPost(post_id, e) {
        return $.ajax({
            url: "/api/posts/" + post_id + "/",
            type: "GET",
            datatype: "json",
            beforeSend: function(){
            },
            success: function(data) {
              if (data) {
                  var httpsUrl = "https://o3e6g3hdp.qnssl.com/"
                  var imageStyle = "-postDetails"
                  var post_thumb_url = httpsUrl + data["post_thumb_url"] + imageStyle;
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
                              src: value["comment_user"]["user_avatar"] ,
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
    
   
    //图片错误时加载备份图片
    
})





