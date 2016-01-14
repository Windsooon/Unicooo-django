$(document).ready(function(){
    $("#add-comment-btn").click(function(){
        var comment_text = $(".comment-form-text").val();
        $.ajax({
            url: "/api/comment/",
            type: "POST",
            datatype: "json",
            data:  {csrfmiddlewaretoken: window.CSRF_TOKEN},
            success: function(data) {
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
              complete:function(){
            },
         });
    })
});
