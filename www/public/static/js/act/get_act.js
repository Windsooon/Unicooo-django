function get_act_list(data, container, page){
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
            var elems = [];
            $.each(data.results, function(key, value){
                if (data.results.length > 0) {
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
                            data-toggle: "modal",
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
                    elems.push($act_outer_container);
                });
                    var $elems = $(elems);
                    var $elems = $(elems).hide();
                    container.append($elems);
                    container.imagesLoaded(function(){
                        $elems.show();
                        container.masonry('appended', $elems); 
                    });
            }
            else {
                console.log("no data");
            }
        },
        complete:function(){
            if (data.next != null) {
                    ajax_state = true;
            }
        }
    });
}
