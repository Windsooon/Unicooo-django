function personal_act(personal, data, page){
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
                act_thumb_url.src = httpsUrl + value["act_thumb_url"] + imageStyle;
                act_thumb_url.setAttribute("onerror", "imgError(this);");
                act_thumb_a.appendChild(act_thumb_url);
                act_thumb_a.appendChild(single_title);
                act_thumb_a.appendChild(single_content);
                act_container.appendChild(act_thumb_a);
                single_title.appendChild(single_title_p);
                single_content.appendChild(single_content_p);
                single_act.appendChild(act_container);
                frag.appendChild(single_act);
            })
            $(".row").append(frag).animate();
        },
        complete:function(){
            if (data.next != null) {
                    ajax_state = true;
            }
        }
    });
}
