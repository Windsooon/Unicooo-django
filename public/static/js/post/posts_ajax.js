$(document).ready(function(){
    var page = 1
    var $container = $('#posts-container').masonry({
        columnWidth: 20,
        itemSelector: '.post-container',
        isFitWidth: true,
        transitionDuration: 0,
    });
    ajax_post(page)
    $(window).scroll(function(){
        //console.log($(window).scrollTop());
        //console.log($(".single-post:last").offset().top);
        if (checkscroll() && ajax_state){
            page += 1;
            ajax_state = false;
            ajax_post(page)
        }
    })

    //post板块进行ajax请求
    function ajax_post(page){
        $.ajax({
            url: "/api/posts/",
            type: "GET",
            datatype: "json",
            data:  {"page": page},
            beforeSend:function(){
            },
            success: function(data) {
                if (data.results.length > 0) {
                    var elems = [];
                    $.each(data.results, function(key, value){
                        var single_post = document.createElement("div");
                        single_post.className = "post-container";
                        //帖子缩略图
                        var post_thumb_a = document.createElement("a");
                        //post_thumb_a.className = value["id"];
                        post_thumb_a.setAttribute("href", "#post_details");
                        post_thumb_a.setAttribute("data-toggle", "modal");
                        post_thumb_a.setAttribute("data-target", "#post-details");
                        post_thumb_a.setAttribute("data-post-id", value["id"]);
                        var post_thumb_url = document.createElement("img");
                        post_thumb_url.src = value["post_thumb_url"];
                        post_thumb_url.setAttribute("onerror", "imgError(this);");
                        //create post border
                        var single_border = document.createElement("div");
                        single_border.className = "post-border";
                        //create post title
                        var single_title = document.createElement("div");
                        single_title.className = "post-title";
                        //create post posttime
                        var single_posttime = document.createElement("div");
                        single_posttime.className = "post-posttime";
                        //create post posttime text
                        var single_posttime_p = document.createElement("p");
                        single_posttime_p.innerHTML = value["post_create_time"];
                        //create post footer
                        var single_footer = document.createElement("div");
                        single_footer.className = "post-footer clearfix";
                        //create post footer content(like and comment count)
                        var single_footer_like = document.createElement("span");
                        single_footer_like.className = "post-like glyphicon glyphicon-heart pull-right";
                        var single_footer_comment = document.createElement("span");
                        single_footer_comment.className = "post-comment glyphicon glyphicon-comment pull-right";
                        //create content div
                        var single_content = document.createElement("div");
                        single_content.className = "post-content";
                        //create post-title text
                        var single_title_p = document.createElement("p");
                        single_title_p.className = "post-user";
                        single_title_p.innerHTML = value["post_user"].user_name;
                        //create post-content text
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
                    $container.append($elems);
                    $container.imagesLoaded(function(){
                        $elems.show();
                        $container.masonry('appended', $elems, true); 
                    });
                }
            },
            complete:function(){
                ajax_state = true;
            }
        });
    }//ajax_postivity结束

    $("#post-details").on("show.bs.modal", function (e) {
        var post_id = $(e.relatedTarget).data('post-id');
        $.ajax({
            url: "/api/post/",
            type: "GET",
            datatype: "json",
            data:  {"post_id": post_id},
            beforeSend:function(){
            },
            success: function(data) {
              if (data.results.length > 0) {
                  $(e.currentTarget).find(".post-raw-details").attr("src",data.results[0]["post_thumb_url"]);
              }
            },
            complete:function(){
            }
        });
    })
    

    //显示剩余输入字数
    $(".comment-form-text").keyup(function(){  
        var $comment_length = $(".comment-form-length");
        var currrent_length=$(".comment-form-text").val().length + 1;   
        if (currrent_length <= 140) {
            $comment_length.text(141-currrent_length);
        }
        else {
            $comment_length.text("beyond 140 char");
            $comment_length.css("color","#3f51b5");
        }

    })  

    function checkscroll(){
        if($(window).scrollTop()+500 > ($(".post-container:last").offset().top)){
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





