var click_url = "http://127.0.0.1:8000/api/acts/";

$("#act-create-btn").on("click", function() {
    ajax_act_create(id, page);
    });


    function ajax_act_create(id, page){
        $.ajax({
            url: click_url,
            type: "GET",
            datatype: "json",
            data:  {"id": user_id},
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
