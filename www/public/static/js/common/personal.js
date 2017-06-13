$(document).ready(function() {
    $('#add-comment-btn').on('click', comment_click_handler);
});

function personalInit(personal, status, page, container){
    if (status == "act_create") {
        data = {"act_author": personal, "page": page};
        get_act_list(data, container);
    }
    else if (status == "act_join") {
        data = {"act_post": personal, "page": page};
        get_act_list(data, container);
    }
    else if (status == "post") {
        data = {"post_author": personal, "page": page};
        get_post_list(data, container);
    }
    else if (status == "feed") {
        data = {"post_feed": personal, "page": page};
        get_post_list(data, container);
    }
}

