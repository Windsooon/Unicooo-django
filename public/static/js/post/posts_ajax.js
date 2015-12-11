$(document).ready(function(){
    var page = 1
    var $container = $("#posts-container");
    var $content = $(".post-container");
    ajax_post(page)
        //$(window).scroll(function(){
    //    //console.log($(window).scrollTop());
    //    //console.log($(".single-post:last").offset().top);
    //    if (checkscroll() && ajax_state){
    //        ajax_state = false;
    //        ajax_postivity(act_type, page)
    //        page += 1;
    //    }
    //})

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
                    var frag = document.createDocumentFragment();
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
                        var single_title = document.createElement("div");
                        single_title.className = "single-title";
                        //活动内容外层div
                        var single_content = document.createElement("div");
                        single_content.className = "single-content-post";
                        //具体活动名称
                        var single_title_p = document.createElement("p");
                        single_title_p.className = "post-title";
                        single_title_p.innerHTML = value["post_title"];
                        //具体活动内容
                        var single_content_p = document.createElement("p");
                        single_content_p.className = "post-content";
                        single_content_p.innerHTML = value["post_content"];
                        post_thumb_a.appendChild(post_thumb_url);
                        single_post.appendChild(post_thumb_a);
                        single_title.appendChild(single_title_p);
                        single_content.appendChild(single_content_p);
                        single_post.appendChild(single_title);
                        single_post.appendChild(single_content);
                        frag.appendChild(single_post);
                    })
                    $container.append($(frag));
                    $container.imagesLoaded(function(){
                        $container.masonry().masonry( 'appended', $(frag), true ); 
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

    //function checkscroll(){
    //    if($(window).scrollTop()+500 > ($(".single-post:last").offset().top)){
    //        return true; 
    //    }
    //    else{
    //        return false;
    //    }
    //}
})


//图片错误时加载备份图片
function imgError(image) {
    image.onerror = "";
    image.src = "../../../static/img/error.png";
    return true;
}


