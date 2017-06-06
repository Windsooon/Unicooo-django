var $act_edit_btn = $("#act-edit-btn");
$act_edit_btn.on("click", function() {
    if ($act_edit_btn.text() == "Edit") {
        var editor = $("#act-editor").data('quill');
        editor.enable();
        $act_edit_btn.text("Save");
        $(".ql-toolbar").css("display", "block");
    }
    else if ($act_edit_btn.text() == "Save") {
        var editor = $("#act-editor").data('quill');

        editor.disable();
        var delta = editor.getContents();
        var act_id = $(".activity-details-content").children('input').val();
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: "/api/acts/" + act_id + "/",
            type: "PATCH",
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken)
            },
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: csrftoken,
                "act_intro": JSON.stringify(delta)},
            success: function(data) {
                $act_edit_btn.text("Edit");
                $(".ql-toolbar").css("display", "none");
            },
        });
    }
});
