$(document).ready(function(){
    $("#id_act_type").on("change", function() {
        var select_val = $("#id_act_type option:selected").val();
        if (select_val == 0) {
            $("#act_type-error").text("Only you can join this activity.But others still can see the activity details by activity id.")
        }
        else if (select_val == 1) {
            $("#act_type-error").text("Group activity won't be shown in frontpage or recommended, but still can be search by activity id.")
        }
        else {
            $("#act_type-error").text("Public activity will show in frontpage.")
        }

    });

    $("#new-act-form :input").prop("disabled", true);
    var formArray = new Array();
    var csrf_token = $("#new-act-form input").eq(0).val();
    $.validator.addMethod(
        "regex",
        function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Act content may only contain alphanumeric characters."
    );
    var validator = $("#new-act-form").validate({
        rules: {
            act_title: {
                required: true,
                minlength: 6,
                maxlength: 30,
                regex: /^((?!'|"|<|>).)*$/,
                remote: {
                    url: "/act_title/",
                    type: "post",
                    data: {
                        csrfmiddlewaretoken: csrf_token,
                        act_title: function() {
                        return $("#act_title").val().trim();
                        },
                        current_user: function() {
                        return $(".request-user").text();
                        }
                    }
                }
            },
            act_content: {
                required: true,
                regex: /^((?!'|"|<|>).)*$/,
                minlength: 6,
            },
        },
        messages: {
            act_title: {
                required: "Please enter your act title.",
                minlength: jQuery.validator.format("Please Enter at least {0} characters."),
                maxlength: jQuery.validator.format("Beyond 30 characters."),
                remote: "You already create this activity."
            },
            act_content: {
                required: "Please enter your act content.",
                minlength: jQuery.validator.format("Please Enter at least {0} characters."),
            },
        },
        submitHandler: function(form) {
            var act_type = $("#id_act_type").val();
            var act_licence = $("#id_act_licence").val();
            var act_title = $("#act_title").val().trim();
            act_title_replace = urlConvert(act_title);
            var act_content = $("#act_content").val();
            var user_name = $(".request-user").text();
            var csrf_token = $("#new-act-form input").eq(0).val();
            var act_url = user_name + "/" + act_title_replace;
            var $form_group_loading = $(".form-group-loading");
            var $form_submit_wrap = $(".submit-btn-wrap");
            csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $("#new-act-form :input").prop("disabled", true);
            $form_submit_wrap.empty()
            var form_outer_loading = $("<div />", {
                          "class": "loading-center",
                      });
            var form_loading = $("<div />", {
                          "class": "la-ball-clip-rotate la-sm",
                      });
            var form_inner_loading = $("<div />");
            form_loading.append(form_inner_loading);
            form_outer_loading.append(form_loading);
            $form_submit_wrap.append(form_outer_loading);
            $.ajax({
                url: "/api/acts/",
                type: "POST",
                datatype: "json",
                data:  {csrfmiddlewaretoken: csrf_token, "act_title": act_title, "act_content": act_content, "act_thumb_url": formArray[1], "act_type": act_type, "act_ident": 20, "act_licence": act_licence, "act_url": act_url},
                beforeSend:function() {},
                success: function(data) {
                    window.location.replace("/act/" + data["act_url"] + "/");
                },
                error: function(xhr, status, error) {
                    $form_submit_wrap.empty();
                    $("#new-act-form :input").prop("disabled", false);
                    if (xhr.status >= 400 && xhr.status < 500) {
                        error_text = "Please check again your input.";
                    }
                    else {
                        error_text = "Please try again later.";
                    }
                    if($(".form-server-error-p").length) {
                        $(".form-server-error-p").text(error_text);
                    }
                    else {
                        var form_server_error = $("<div />", {
                          "class": "form-server-error"
                        });
                        $form_server_error_span = $("<span />", {"class": "pull-left form-server-error-span glyphicon glyphicon-exclamation-sign"});
                        $form_server_error_p = $("<p />", {"class": "form-server-error-p", text: error_text});
                        $form_server_error_span.appendTo(form_server_error).hide().fadeIn();
                        $form_server_error_p.appendTo(form_server_error).hide().fadeIn();
                        $form_submit_wrap.before(form_server_error);
                    }
                    var form_submit_button = $("<button />", {"class": "submit-btn btn btn-primary btn-block"});
                    var form_submit_button_span = $("<span />", {"class": "glyphicon glyphicon-ok"});
                    form_submit_button.append(form_submit_button_span);
                    $form_submit_wrap.append(form_submit_button);
                },
            });
        },
        success: function(label) {
        },
        highlight: function(element, errorClass) {
            $(element).parent().next().find("." + errorClass).removeClass("checked");
        }
    });

    var formData = new FormData();
    var formArray = new Array();
    $act_cover_span = $("#act-cover-span");
    $('#act-cover-image').on("click", function(){ 
        formData = new FormData();
        formArrar = new Array();
        $.ajax({
            url: "/token",
            type: "GET",
            datatype: "json",
            data: {"type": 0},
            success: function(data) {
                formData.append("token", data["token"]);
                formData.append("key", data["key"]);
                formArray[0] = data["token"];
                formArray[1] = data["key"];
            },
        });
    });

    $('#act-cover-image').on("change", function(){ 
        if (typeof (FileReader) != "undefined") {
            var image_holder = $(".act-upload-div");
            image_holder.empty();
            var reader = new FileReader();
            reader.onload = function (e) {
                $("<img />", {
                    "src": e.target.result,
                    "class": "unfinished-image",
                    "id": "act-upload-img"
                }).appendTo(image_holder);

            }
            image_holder.show();
            reader.readAsDataURL($(this)[0].files[0]);
        } 
        else {
            console.log("This browser does not support FileReader.");
        }
        var file = this.files[0];
        $("#new-act-form :input").prop("disabled", false);
        formData.append("file", file);
        $.ajax({
            xhr: function() {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", function(evt) {
                  if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    percentComplete = parseInt(percentComplete * 100);
                    $(".progress-bar").css("width", percentComplete + "%")
                    if (percentComplete === 100) {
                    }
                  }
                }, false);
                return xhr;
            },  
            url: "https://up.qbox.me",
            type: "POST",
            data: formData,
            datatype: "json",
            cache: false,
            processData: false, 
            contentType: false,
            beforeSend:function(){
               $act_cover_span.empty(); 
               $("#act-cover-btn").prop("disabled", true);
               var act_outer_loading = $("<div />", {
                          "class": "",
                      });
               var act_loading = $("<div />", {
                          "class": "la-ball-clip-rotate la-sm",
                      });
               var act_inner_loading = $("<div />");
               act_loading.append(act_inner_loading);
               act_outer_loading.append(act_loading);
               $act_cover_span.append(act_outer_loading);
            },
            error: function(xhr, status, error) {
                if (xhr.status >= 400 && xhr.status < 500) {
                        error_text = "Please check again your input.";
                }
                else {
                    error_text = "Please try again later.";
                }
                $act_cover_span.empty(); 
                $act_cover_span.html(error_text);
                var upload_failed = $("<input>").attr({
                            "class": "cropit-image-input", 
                            type: "file",
                            id: "act-cover-image",
                        });                  
                upload_failed.appendTo($act_cover_span).hide().fadeIn(500);
            },
            success: function(data) {
                $("#act-cover-btn").prop("disabled", false);
                $act_cover_span.empty(); 
                var upload_success = $("<span />", {
                          text: "Success",
                      });
                upload_success.appendTo($act_cover_span).hide().fadeIn(500);
             },
            complete: function() {
                $("#act-upload-img").removeClass("unfinished-image");
                $("#act-upload-img").addClass("finished-image");
            },
        });
    });
});
