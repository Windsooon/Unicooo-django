$(document).ready(function() {
});

function personalInit(personal, status){
    var page = 1;
    if (status == "act_create") {
        data = {"act_author": personal};
        personal_act(personal, data, page);
    }
    else if (status == "act_join") {
        data = {"act_post": personal};
        personal_act(personal, data, page);
    }
    else {
        var $container = $('.row').masonry({
            columnWidth: 20,
            itemSelector: '.post-container',
            isFitWidth: true,
            transitionDuration: 0,
        });
        var ajax_state = false;
        personal_post(personal, page, $container);
    }
}

function personal_act(personal, data, page){
    $.ajax({
        url: "http://127.0.0.1:8000/api/acts/",
        type: "GET",
        datatype: "json",
        data: data,
        beforeSend:function(){
        },
        success: function(data) {
            var frag = document.createDocumentFragment();
            $.each(data.results, function(key, value){
                var single_act = document.createElement("div");
                single_act.className = "single-act col-sm-6 col-md-4 col-lg-4"
                var act_container = document.createElement("div");
                act_container.className = "act-container";
                //活动缩略图
                var act_thumb_a = document.createElement("a");
                act_thumb_a.className = "thumbnail act-thumb-a";
                act_thumb_a.setAttribute("href", "/act/" + value["act_user"]["user_name"] + "/" + value["act_title"]);
                act_thumb_a.setAttribute("data-toggle", "modal");
                var act_thumb_url = document.createElement("img");
                //活动名称外层div
                var single_title = document.createElement("div");
                single_title.className = "single-title";
                //活动内容外层div
                var single_content = document.createElement("div");
                single_content.className = "single-content";
                //具体活动称
                var single_title_p = document.createElement("p");
                single_title_p.className = "act-title";
                single_title_p.innerHTML = value["act_title"];
                //具体活动内容
                var single_content_p = document.createElement("p");
                single_content_p.className = "act-content";
                single_content_p.innerHTML = value["act_content"];
                act_thumb_url.src = value["act_thumb_url"];
                act_thumb_url.setAttribute("onerror", "imgError(this);");
                act_thumb_a.appendChild(act_thumb_url);
                act_thumb_a.appendChild(single_title);
                act_thumb_a.appendChild(single_content);
                act_container.appendChild(act_thumb_a);
                single_title.appendChild(single_title_p);
                single_content.appendChild(single_content_p);
                single_act.appendChild(act_container);
                frag.appendChild(single_act);
            })
            $(".row").append(frag).animate();
        },
        complete:function(){
            ajax_state = true;
        }
    });
}//ajax_act结束


//post板块进行ajax请求
function personal_post(personal, page, container){
    $.ajax({
        url: "/api/posts/",
        type: "GET",
        datatype: "json",
        data:  {"post_author": personal, "page": page},
        beforeSend:function(){
        },
        success: function(data) {
            if (data.results.length > 0) {
                var elems = [];
                $.each(data.results, function(key, value){
                    var single_post = document.createElement("div");
                    single_post.className = "post-container";
                    //post thumb image
                    var post_thumb_a = document.createElement("a");
                    //post_thumb_a.className = value["id"];
                    post_thumb_a.setAttribute("href", "#post_details");
                    post_thumb_a.setAttribute("data-toggle", "modal");
                    post_thumb_a.setAttribute("data-target", "#post-details");
                    post_thumb_a.setAttribute("data-post-id", value["id"]);
                    var post_thumb_url = document.createElement("img");
                    post_thumb_url.src = value["post_thumb_url"];
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
                    single_posttime_p.innerHTML = value["post_create_time"];
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
                    single_post.appendChild(post_thumb_a);
                    single_posttime.appendChild(single_posttime_p);
                    single_title.appendChild(single_title_p);
                    single_footer.appendChild(single_footer_like);
                    single_footer.appendChild(single_footer_comment);
                    single_content.appendChild(single_content_p);
                    //single_border
                    single_border.appendChild(single_title);
                    single_border.appendChild(single_posttime);
                    //single_post
                    single_post.appendChild(single_border);
                    single_post.appendChild(single_content);
                    single_post.appendChild(single_footer);
                    elems.push(single_post);
                })
                var $elems = $(elems);
                var $elems = $(elems).hide();
                container.append($elems);
                container.imagesLoaded(function(){
                    $elems.fadeIn(500);
                    container.masonry('appended', $elems); 
                });
            }
            else {
                console.log("nothing"); 
            }
        },
        complete:function(){
            ajax_state = true;
        }
    });
}//ajax_post end


$("#post-details").on("show.bs.modal", function(e) {
        var post_id = $(e.relatedTarget).data('post-id');
        getPost(post_id, e, getId);
    });

function getPost(post_id, e, getId) {
        return $.ajax({
            url: "/api/posts/" + post_id + "/",
            type: "GET",
            datatype: "json",
            beforeSend: function(){
            },
            success: function(data) {
              if (data) {
                  getId(data);
                  var elems = [];
                  $(".list-group").empty();
                  $(e.currentTarget).find(".post-raw-details").attr("src",data["post_thumb_url"]);
                  $(".post-user").text(data["post_user"]["user_name"]);
                  $(".post-posttime p").text(data["post_creattime"]);
                  $(".post-content-p").text(data["post_content"]);
                  $.each(data["post_comment"], function(key, value){
                      //comment avatar
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

                      var comment_username = $("<div />", {
                          "class": "comment-username",
                      });

                      var comment_posttime_span = $("<span />", {
                          text: value["comment_create_time"],
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
                          text:  value["comment_content"],
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
                      
                      $(".list-group").append(list_group_item);
                  });
              }
            },
            complete:function(){
            }
        });
    }

//get current post id and user id
    function getId(data) {
        //comment_click_handler is in comment_ajax.js
        var user_id = data["user"];
        var post_id = data["id"];
        $('#add-comment-btn').one('click', {"user_id": user_id, "post_id": post_id}, comment_click_handler);
    }



