$(document).ready(function(){
    var ajax_state = true
    if (checkscroll() && ajax_state){
        ajax_state = false;
        ajax_activity(id, page, number)
    }

})

//检查滚动条是否到达底部2/3位置
function checkscroll(){
        var 
        if (){
            return true; 
        }
        else{
            return false;
        }
    }

//activity板块进行ajax请求
function ajax_activity(id, page, number){
    $.ajax({
        url: "/activity/
        type: "GET",
        datatype: "json",
        data:  {"id": id, "page": page, "number": number},
        beforeSend:function(){
            console.log("load image");
        }
        success: function(data) {
            console.log(data);      
        },
        complete:function(){
            ajax_state = true;
        }
    });
}

