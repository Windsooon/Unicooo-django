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
            url: "/api/post/",
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
                        var post_thumb_url = document.createElement("img");
                        post_thumb_url.src = value["post_thumb_url"];
                        post_thumb_url.setAttribute("onerror", "imgError(this);");
                        //活动名称外层div
                        var single_border = document.createElement("div");
                        single_border.className = "post-border";
                        var single_title = document.createElement("div");
                        single_title.className = "post-title";
                        var single_posttime = document.createElement("div");
                        single_posttime.className = "post-posttime";
                        var single_posttime_p = document.createElement("p");
                        single_posttime_p.innerHTML = value["post_create_time"];
                        //活动内容外层div
                        var single_content = document.createElement("div");
                        single_content.className = "post-content";
                        //具体活动名称
                        var single_title_p = document.createElement("p");
                        single_title_p.className = "post-user";
                        single_title_p.innerHTML = value["post_user"].user_name;
                        //具体活动内容
                        var single_content_p = document.createElement("p");
                        single_content_p.className = "post-content-p";
                        single_content_p.innerHTML = value["post_content"];
                        post_thumb_a.appendChild(post_thumb_url);
                        single_post.appendChild(post_thumb_a);
                        single_posttime.appendChild(single_posttime_p);
                        single_title.appendChild(single_title_p);
                        single_content.appendChild(single_content_p);
                        single_border.appendChild(single_title);
                        single_border.appendChild(single_posttime);
                        single_post.appendChild(single_border);
                        single_post.appendChild(single_content);
                        elems.push(single_post);
                    })
                    var $elems = $(elems);
                    $container.append($elems);
                    $container.imagesLoaded(function(){
                        $container.masonry('appended', $elems, true); 
                    });
                }
            },
            complete:function(){
                ajax_state = true;
            }
        });
    }//ajax_postivity结束

    $('#post_details').on('show.bs.modal', function (e) {
        var post_target = e.relatedTarget;
        post_id = act_target.className.split(" ");
        post_id = act_id[act_id.length-1];
        $.ajax({
            url: "/api/post/",
            type: "GET",
            datatype: "json",
            data:  {"post_id": act_id},
            beforeSend:function(){
            },
            success: function(data) {
            },
            complete:function(){
            }
        });
    })

    function checkscroll(){
        if($(window).scrollTop()+500 > ($(".post-container:last").offset().top)){
            return true; 
        }
        else{
            return false;
        }
    }
})


//图片错误时加载备份图片
function imgError(image) {
    image.onerror = "";
    image.src = "../../../static/img/error.png";
    return true;
}


