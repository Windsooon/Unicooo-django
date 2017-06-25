function get_act_list(data, container, out=false, text=false){
    $.ajax({
        url: "/api/acts/",
        type: "GET",
        datatype: "url",
        data: data,
        beforeSend:function(){
        },
        success: function(data) {
            var imageStyle = "-actCoverSmall"
            if (data.results.length == 0 && out && text) {
                var $empty_div = $("<div />", {
                        "class": "comment-wrapper well col-lg-8 col-lg-offset-2",
                        });
                var $empty_text = $("<p />", {
                          "id": "feed-empty",
                          "text": text,
                      });
                $empty_div.append($empty_text);
                out.append($empty_div);
            }
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
                            href: "/act/" + value["act_url"] + "/",
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
                });
            }
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


function get_post_list(data, container, out=false, text=false){
    $.ajax({
        url: "/api/posts/",
        type: "GET",
        datatype: "json",
        data:  data,
        beforeSend:function(){
           if (!$(".outer_loading").length) {
               var post_outer_loading = $("<div />", {
                          "class": "outer_loading",
                      });
               $("#posts-container").append(post_outer_loading);
               loadingBefore(post_outer_loading, "la-md");
           }
        },
        success: function(data) {
            if (data.results.length == 0 && out && text) {
                var $empty_div = $("<div />", {
                        "class": "comment-wrapper well col-lg-8 col-lg-offset-2",
                        });
                var $empty_text = $("<p />", {
                          "id": "feed-empty",
                          "text": text,
                      });
                $empty_div.append($empty_text);
                out.append($empty_div);
            }
            if (data.results.length > 0) {
                var httpsUrl = "https://o3e6g3hdp.qnssl.com/"
                var imageStyle = "-postList"
                var elems = [];
                $.each(data.results, function(key, value){
                    var date = value["post_create_time"].split("T", 1);
                    var single_post = document.createElement("div");
                    single_post.className = "post-container col-xs-12 col-sm-6 col-md-4 col-lg-4";
                    single_post.setAttribute("id", "post-" + value["id"]);
                    //post container col
                    var single_post_col = document.createElement("div");
                    single_post_col.className = "post-container-col";
                    //post thumb image
                    var post_thumb_a = document.createElement("a");
                    post_thumb_a.className = "post-thumb-a";
                    post_thumb_a.setAttribute("href", "#post_details");
                    post_thumb_a.setAttribute("data-toggle", "modal");
                    post_thumb_a.setAttribute("data-target", "#post-details");
                    post_thumb_a.setAttribute("data-post-id", value["id"]);
                    //delete buttton
                    
                    //if post is image
                    if (value["post_mime_types"] == 0) {
                        var post_thumb_url = document.createElement("img");
                        post_thumb_url.src = httpsUrl + value["post_thumb_url"] + imageStyle;
                        post_thumb_url.setAttribute("onerror", "imgError(this);");
                        post_thumb_a.appendChild(post_thumb_url);
                    }
                    else if  (value["post_mime_types"] == 1) {
                        var audio_div = document.createElement("div");
                        audio_div.className = "audio-div";
                        var audio_div_wrapper = document.createElement("div");
                        audio_div_wrapper.className = "audio-div-wrapper";
                        var fade_out = document.createElement("div");
                        fade_out.className = "act-fadeout";
                        // audio content
                        var audio_div_p = document.createElement("p");
                        var audio_div_audio = document.createElement("audio");
                        audio_div_audio.className = "audio-div-audio";
                        audio_div_audio.src = httpsUrl + value["post_thumb_url"];
                        audio_div_audio.setAttribute("controls", "controls");
                        audio_div_audio.setAttribute("preload", "auto");
                        if (value["post_content"].length <= 10) {
                            audio_div_p.className = "audio-div-p";
                        }
                        else {
                            audio_div_p.className = "audio-div-p-small";
                        }
                        audio_div_p.innerHTML = value["post_content"];
                        audio_div.appendChild(audio_div_p);
                        audio_div_wrapper.appendChild(audio_div)
                        post_thumb_a.appendChild(audio_div_wrapper);
                        post_thumb_a.appendChild(fade_out);
                        post_thumb_a.appendChild(audio_div_audio);

                    }
                    //post border
                    var single_border = document.createElement("div");
                    single_border.className = "post-border";
                    //post title
                    var single_title = document.createElement("div");
                    single_title.className = "post-title";
                    //post title a
                    var single_title_a = document.createElement("a");
                    single_title_a.className = "post-title-a";
                    single_title_a.setAttribute("href", "/" + value["post_author"] + "/act_create" );
                    //post posttime
                    var single_posttime = document.createElement("div");
                    single_posttime.className = "post-posttime";
                    //post posttime text
                    var single_posttime_p = document.createElement("p");
                    single_posttime_p.className = "post-posttime-p";
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
                    if (value["likes"] != 0) {
                        single_footer_like_p.innerHTML = value["likes"];
                    }
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
                    single_posttime.appendChild(single_posttime_p);
                    single_title.appendChild(single_title_p);
                    single_title_a.appendChild(single_title);
                    //footer like and p
                    single_footer_like.appendChild(single_footer_like_p);
                    single_footer_comment.appendChild(single_footer_comment_p) ;
                    single_footer.appendChild(single_footer_like);
                    single_footer.appendChild(single_footer_comment);
                    single_content.appendChild(single_content_p);
                    //single_border
                    single_border.appendChild(single_title_a);
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
                    $(".outer_loading").fadeOut(150, function(){
                        $(this).remove();
                    });
                    $elems.show();
                    container.masonry('appended', $elems); 
                });
            }
        },
        complete:function(data){
            $(".outer_loading").fadeOut(150, function() {
                $(this).remove();
            });
            complete_data = $.parseJSON(data.responseText); 
            if (complete_data.next) {
                ajax_state = true;
            }
        }
    });
}
//end get_post_list

