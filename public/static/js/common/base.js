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
                        window.location.replace("/act/"+value["act_author"]+"/"+value["act_title"]);
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




