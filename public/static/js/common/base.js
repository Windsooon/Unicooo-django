var httpsUrl = "https://o3e6g3hdp.qnssl.com/";

$(document).ready(function() {
    //click get comments
    $(".base-comments").on("click", function() {
        if ($(".base-circle").length > 0) {
            $(".base-circle").remove();
            $.ajax({
                url: "/sub_no",
                type: "GET",
            });
        }    
    });
    //press enter still search the act
    $('.act-search-text').keypress(function (e) {
        var key = e.which;
        if(key == 13)  // the enter key code
        {
            $(".act-search").click();
            return false;  
        }
    });   
    // serach acd by act_id
    $(".act-search").on("click", function() {
        act_id = parseInt($(".act-search-text").val(), 10);
        if (act_id < 10000) {
            act_id = 0
        }
        else {
            act_id = act_id - 10000;
        }
        $.ajax({
            url: "/api/acts/",
            dataType: "json",
            data: {"act_id": act_id},
            type: "GET",
            success: function(data) {
                if (data.results.length > 0) {
                    $.each(data.results, function(key, value){
                        console.log(value["act_url"]);
                        window.location.replace("/act/" + value["act_url"]);
                    })
                }
            },
            error: function() {
            }
        });
    });
});

function poll() {
	var poll_interval=0;
	$.ajax({
		url: "/sub/",
		type: "GET",
		dataType: "json",
        statusCode: {
            200: function(response) {
                append_circle(); 
            }
        },
		success: function(data, xhr) {
		},
		error: function () {
		},
		complete: function () {
			poll_interval=90000;
			setTimeout(poll, poll_interval);
		},
	});
}

function append_circle() {
    if ($(".base-circle").length < 1) {
        var circle = $("<span />", {
            "class": "base-circle",
        })
        $(".base-comments").append(circle);
    }
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function checkScroll(outerContainer, innerContainer){
    if($(window).scrollTop() > Math.round(outerContainer.height()*2/5)){
        return true; 
    }
    else{
        return false;
    }
}

function imgError(image) {
    image.onerror = "";
    image.src = "../../static/img/error.png";
    return true;
}

function loadingBefore(outer_div) {
    outer_div.empty();
    var outer_loading = $("<div />");
    var normal_loading = $("<div />", {
               "class": "la-ball-clip-rotate la-sm",
           });
    var inner_loading = $("<div />");
    normal_loading.append(inner_loading);
    outer_loading.append(normal_loading);
    outer_div.append(outer_loading);
}

function loadingAfter(outer_div, text_code) {
    switch(text_code){
        case 1:
          text = "SUCCESS";
          break;
        case 2:
          text = "PLEASE TRY AGAIN LATER";
          break;
        default:
    }
    outer_div.empty(); 
    var upload_text = $("<span />", {
               text: text,
           });
    upload_text.appendTo(outer_div).hide().fadeIn(500);
}

function urlConvert(string) {
    string = string.replace(/,|<|>|{|}|。|，/g, ' ').replace(/\s+/g, ' ').trim().replace(/\s+/g, '-');
    return string;
}
