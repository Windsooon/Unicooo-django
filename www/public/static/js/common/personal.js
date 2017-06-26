$(document).ready(function() {
    $('#add-comment-btn').on('click', comment_click_handler);
});

function personalInit(personal, status, page, container){
    if (status == "act_create") {
        data = {"act_author": personal, "page": page};
        get_act_list(data, container, $(".activity-row"), "You haven't create any activities yet.");
    }
    else if (status == "act_join") {
        data = {"act_post": personal, "page": page};
        get_act_list(data, container, $(".activity-row"), "You haven't join any activities yet.");
    }
    else if (status == "post") {
        data = {"post_author": personal, "page": page};
        get_post_list(data, container, $(".posts-container"), "You haven't join any activities yet.");
    }
    else if (status == "feed") {
        data = {"post_feed": personal, "page": page};
        get_post_list(data, container, $(".post-list"), "You haven't join any activities yet.");
    }
}

