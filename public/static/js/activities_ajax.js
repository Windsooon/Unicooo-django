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
            console.log("scroll");
            console.log($(window).scrollTop());
            console.log(Math.floor($(window).height()*3/4));
            ajax_activity(act_type, page, 6)
        }
    })
    

})


//检查滚动条是否到达底部2/3位置
function checkscroll(){
    if($(window).scrollTop() > Math.floor($(window).height()*3/4)){
        return true; 
    }
    else{
        return false;
    }
}

//activity板块进行ajax请求
function ajax_activity(act_type, page, number){
    $.ajax({
        url: "/act/activities/",
        type: "GET",
        datatype: "json",
        data:  {"act_type": act_type, "page": page, "number": number},
        beforeSend:function(){
            console.log("load image");
        },
        success: function(data) {
            //console.log(data);      
        },
        complete:function(){
            ajax_state = true;
            page += 1;
        }
    });
}


//图片错误时加载备份图片
function imgError(image) {
    image.onerror = "";
    image.src = "../../static/img/error.png";
    return true;
}

