$(document).ready(function(){
    //设置不同活动的按钮颜色
    var act_list = window.location.pathname.split("/")[2];
    act_btn = act_list + "-btn";
    switch (act_list)
    {
    case "public":
      act_type = 0
      break;
    case "group":
      act_type = 1
      break;
    case "personal":
      act_type = 2
      break;
    }
    $("#"+act_btn).removeClass("btn-default");
    $("#"+act_btn).addClass("btn-primary");
    var ajax_state = true
    var page = 1
    $(window).scroll(function(){
        if (checkscroll() && ajax_state){
            ajax_state = false;
            ajax_activity(act_type, page)
            page += 1;
        }
    })

    //activity板块进行ajax请求
    function ajax_activity(act_type, page){
        $.ajax({
            url: "/api/act/",
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
                    act_thumb_a.className = "thumbnail " + value["id"];
                    act_thumb_a.setAttribute("href", "#act_details");
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
                    act_container.appendChild(act_thumb_a);
                    single_title.appendChild(single_title_p);
                    single_content.appendChild(single_content_p);
                    act_container.appendChild(single_title);
                    act_container.appendChild(single_content);
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

