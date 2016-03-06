function get_act_list(data, container){
    $.ajax({
        url: "/api/acts/",
        type: "GET",
        datatype: "json",
        data: data,
        beforeSend:function(){
        },
        success: function(data) {
            var httpsUrl = "https://o3e6g3hdp.qnssl.com/"
            var imageStyle = "-actCoverSmall"
            if (data.results.length > 0) {
                $.each(data.results, function(key, value){
                    //outer single act div
                    var $act_outer_container = $("<div />", {
                            "class": "act-outer-container col-sm-6 col-md-4 col-lg-4",
                            });
                    //inner single act div
                    var $act_inner_container = $("<div />", {
                            "class": "act-inner-container",
                            });
                    //act thumb image
                    var $act_thumb_a = $("<a />", {
                            "class": "act-thumb-a",
                            href: "/act/" + value["act_user"]["user_name"] + "/" + value["act_title"],
                            "data-toggle": "modal",
                            });
                    var $act_thumb_img = $("<img />", {
                            "class": "act-thumb-img",
                            src: httpsUrl + value["act_thumb_url"] + imageStyle,
                            onerror: "imgError(this);",
                            });
                    //act title
                    var $act_title_wrapper = $("<div />", {
                            "class": "act-title-wrapper",
                            });
                    var $act_title_p = $("<p />", {
                            "class": "act-title-p",
                            text: value["act_title"],
                            });
                    //act content
                    var $act_content_wrapper = $("<div />", {
                            "class": "act-content-wrapper",
                            });
                    var $act_content_p = $("<p />", {
                            "class": "act-content-p",
                            text: value["act_content"],
                            });
                    //act title append
                    $act_title_wrapper.append($act_title_p); 
                    //act content append
                    $act_content_wrapper.append($act_content_p); 
                    //act thumb append
                    $act_thumb_a.append($act_thumb_img);
                    $act_thumb_a.append($act_title_wrapper);
                    $act_thumb_a.append($act_content_wrapper);
                    //act inside div append
                    $act_inner_container.append($act_thumb_a);
                    $act_outer_container.append($act_inner_container);
                    $act_outer_container.appendTo(container).hide().fadeIn();
                    //container.masonry( 'appended', $act_outer_container )
                });
            }
            else {
            }
            //end for each
            //container.imagesLoaded(function(){
            //    $elems.show();
            //    container.masonry('appended', $elems); 
            //});
        },
        complete:function(data){
            var complete_data = $.parseJSON(data.responseText); 
            if (complete_data.next) {
                ajax_state = true;
            }
        }
    });
}
//end function get_act_list


function get_post_list(data, container){
    $.ajax({
        url: "/api/posts/",
        type: "GET",
        datatype: "json",
        data:  data,
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
                    single_footer_like.className = "post-like glyphicon glyphicon-heart";
                    var single_footer_comment = document.createElement("span");
                    single_footer_comment.className = "post-comment glyphicon glyphicon-comment";
                    var single_footer_comment_p = document.createElement("p");
                    single_footer_comment_p.className = "post-comment-p";
                    if (value["comment_count"] != 0) {
                        single_footer_comment_p.innerHTML = value["comment_count"];
                    }
                    var single_footer_like_p = document.createElement("p");
                    single_footer_like_p.className = "post-like-p"
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
                    //footer like and p
                    single_footer_like.appendChild(single_footer_like_p);
                    single_footer_comment.appendChild(single_footer_comment_p) ;
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
            complete_data = $.parseJSON(data.responseText); 
            if (complete_data.next) {
                ajax_state = true;
            }
        }
    });
}
//end get_post_list

function checkScroll(innerContainer){
    if($(window).scrollTop()+500 > (innerContainer.last().offset().top)){
        return true; 
    }
    else{
        return false;
    }
}


