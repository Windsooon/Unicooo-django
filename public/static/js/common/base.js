function poll() {
	var poll_interval=0;

	$.ajax({
		url: "/sub",
		type: 'GET',
		dataType: 'json',
		success: function(data) {
            append_circle();
			poll_interval=0;
		},
		error: function () {
			poll_interval=1000;
		},
		complete: function () {
			setTimeout(poll, poll_interval);
		},
	});
}

function append_circle() {
    var circle = $("<span />", {
        "class": "base-circle",
    })
    $(".base-comments").append(circle);
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




