$(document).ready(function(){
    var page = 1
    var scrollTimeout;
    $activity_input = $(".activity-details-content input");
    var act_id = $activity_input.eq(0).val();
    var $container = $('#posts-container').masonry({
        columnWidth: 20,
        itemSelector: '.post-container',
        transitionDuration: '0.3s',
        hiddenStyle: { opacity: 0 },
        visibleStyle: { opacity: 1 }
    });
    var ajax_state = false;
    ajax_post(page)
    $(window).scroll(function () {
        if (scrollTimeout) {
            clearTimeout(scrollTimeout);
            scrollTimeout = null;
        }
        scrollTimeout = setTimeout(scrollHandler, 50);
    });
    scrollHandler = function () {
        // Check your page position
        if (checkScroll() && ajax_state) {
            page += 1;
            ajax_state = false;
            ajax_post(page);
        }
    };


    
    $("#post-details").on("show.bs.modal", function(e) {
        var post_id = $(e.relatedTarget).data('post-id');
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
                  $(".post-details-user").text(data["post_user"]["user_name"]);
                  $(".post-details-posttime").text(post_date);
                  $(".post-details-content-p").text(data["post_content"]);
                  $.each(data["post_comment"], function(key, value){
                      //comment avatar
                      var date = value["comment_create_time"].split("T", 1);
                      var comment_avatar_s = $("<img />", {
                          src: value["comment_user"]["user_avatar"] ,
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
                          href:  value["comment_user"]["user_name"],
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
    
    
    //get post per page
    function ajax_post(page){
        $.ajax({
            url: "/api/posts/",
            type: "GET",
            datatype: "json",
            data:  {"act_id": act_id, "page": page},
            beforeSend:function(){
               var post_outer_loading = $("<div />", {
                          "class": "outer_loading",
                      });
               var post_loading = $("<div />", {
                          "class": "la-ball-clip-rotate",
                      });
               var post_inner_loading = $("<div />");
               post_loading.append(post_inner_loading);
               post_outer_loading.append(post_loading);
               //$("#posts-container").after(post_outer_loading);
            },
            success: function(data) {
                if (data.results.length > 0) {
                    var httpsUrl = "https://o3e6g3hdp.qnssl.com/"
                    var imageStyle = "-postList"
                    var elems = [];
                    $.each(data.results, function(key, value){
                        var date = value["post_create_time"].split("T", 1);
                        var single_post = document.createElement("div");
                        single_post.className = "post-container col-xs-12 col-sm-6 col-md-6 col-lg-4";
                        //post container col
                        var single_post_col = document.createElement("div");
                        single_post_col.className = "post-container-col";
                        //post thumb image
                        var post_thumb_a = document.createElement("a");
                        //post_thumb_a.className = value["id"];
                        post_thumb_a.setAttribute("href", "#post_details");
                        post_thumb_a.setAttribute("data-toggle", "modal");
                        post_thumb_a.setAttribute("data-target", "#post-details");
                        post_thumb_a.setAttribute("data-post-id", value["id"]);
                        var post_thumb_url = document.createElement("img");
                        post_thumb_url.src = httpsUrl + value["post_thumb_url"] + imageStyle;
                        post_thumb_url.setAttribute("onerror", "imgError(this);");
                        //post border
                        var single_border = document.createElement("div");
                        single_border.className = "post-border";
                        //post title
                        var single_title = document.createElement("div");
                        single_title.className = "post-title";
                        //post posttime
                        var single_posttime = document.createElement("div");
                        single_posttime.className = "post-posttime";
                        //post posttime text
                        var single_posttime_p = document.createElement("p");
                        single_posttime_p.innerHTML = date;
                        //post footer
                        var single_footer = document.createElement("div");
                        single_footer.className = "post-footer clearfix";
                        //post footer content(like and comment count)
                        var single_footer_like = document.createElement("span");
                        single_footer_like.className = "post-like glyphicon glyphicon-heart pull-right";
                        var single_footer_comment = document.createElement("span");
                        single_footer_comment.className = "post-comment glyphicon glyphicon-comment pull-right";
                        //content div
                        var single_content = document.createElement("div");
                        single_content.className = "post-content";
                        //post-title text
                        var single_title_p = document.createElement("p");
                        single_title_p.className = "post-user";
                        single_title_p.innerHTML = value["post_user"].user_name;
                        //post-content text
                        var single_content_p = document.createElement("p");
                        single_content_p.className = "post-content-p";
                        single_content_p.innerHTML =  value["post_content"];
                        post_thumb_a.appendChild(post_thumb_url);
                        single_posttime.appendChild(single_posttime_p);
                        single_title.appendChild(single_title_p);
                        single_footer.appendChild(single_footer_like);
                        single_footer.appendChild(single_footer_comment);
                        single_content.appendChild(single_content_p);
                        //single_border
                        single_border.appendChild(single_title);
                        single_border.appendChild(single_posttime);
                        //single_post
                        single_post_col.appendChild(post_thumb_a);
                        single_post_col.appendChild(single_border);
                        single_post_col.appendChild(single_content);
                        single_post_col.appendChild(single_footer);
                        single_post.appendChild(single_post_col);
                        elems.push(single_post);
                    })
                    var $elems = $(elems);
                    var $elems = $(elems).hide();
                    $container.append($elems);
                    $container.imagesLoaded(function(){
                        $elems.show();
                        $container.masonry('appended', $elems); 
                    });
                }
                else {
                }
            },
            complete:function(data){
                if (data.next != null) {
                    ajax_state = true;
                }
            }
        });
    }//ajax_post end
    
   
    function checkScroll(){
        if($(window).scrollTop()+400 > ($(".post-container:last").offset().top)){
            return true; 
        }
        else{
            return false;
        }
    }

    //图片错误时加载备份图片
    function imgError(image) {
        image.onerror = "";
        image.src = "../../../static/img/error.png";
        return true;
    }

})





