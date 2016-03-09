$(document).ready(function() {
    $('#add-comment-btn').on('click', comment_click_handler);
});

function personalInit(personal, status, page, container){
    if (status == "act_create") {
        data = {"act_author": personal, "page": page};
        get_act_list(data, container);
    }
    else if (status == "act_join") {
        data = {"act_post": personal, "page": page};
        get_act_list(data, container);
    }
    else {
        data = {"post_author": personal, "page": page};
        get_post_list(data, container);
    }
}




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
                    container.append($elems);
                    container.imagesLoaded(function(){
                        $elems.show();
                        container.masonry('appended', $elems); 
                    });
                }
                else {
                }
            },
            complete:function(data){
                //$(".outer_loading").remove();
                if (data.next != null) {
                    ajax_state = true;
                }
            }
        });
    }//ajax_post end


$("#post-details").on("show.bs.modal", function(e) {
        var post_id = $(e.relatedTarget).data('post-id');
        getPost(post_id, e);
    });

