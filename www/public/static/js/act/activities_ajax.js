$(document).ready(function(){
    ajax_activity(0, 1);
    var ajax_state = true
    var page = 1
    $(window).scroll(function(){
        if (checkscroll() && ajax_state){
            ajax_state = false;
            ajax_activity(0, page)
            page += 1;
        }
    })

    //activity板块进行ajax请求
    function ajax_activity(act_type, page){
        $.ajax({
            url: "/api/acts/",
            type: "GET",
            datatype: "json",
            data:  {"act_type": act_type, "page": page},
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
                    //活动fadeout
                    var fade_out = document.createElement("div");
                    fade_out.className = "fadeout";
                    //活动内容外层div
                    var single_content = document.createElement("div");
                    single_content.className = "single-content";
                    //具体活动
                    var single_title_p = document.createElement("p");
                    single_title_p.className = "act-title";
                    single_title_p.innerHTML = value["act_title"];
                    //活动作者
                    var act_author = document.createElement("p");
                    act_author.className = "act-author pull-right";
                    act_author.innerHTML = value["act_user"]["user_name"];
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
                    single_content.appendChild(fade_out);
                    single_act.appendChild(act_container);
                    frag.appendChild(single_act);
                })
                $(".row").append(frag).animate();
            },
            complete:function(){
                ajax_state = true;
            }
        });
    }//ajax_activity结束

    function checkscroll(){
        if($(window).scrollTop()+500 > ($(".single-act:last").offset().top)){
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
    image.src = "../../static/img/error.png";
    return true;
}

