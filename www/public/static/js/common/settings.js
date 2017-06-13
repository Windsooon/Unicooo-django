$(document).ready(function() {
   formArray = new Array();
   $.validator.addMethod(
        "regex",
        function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Details may only contain alphanumeric characters."
    );
   var validator = $("#settings-form").validate({
        rules: {
            user_details: {
                required: true,
                regex: /^((?!'|"|<|>).)*$/,
                minlength: 10,
            },
        },
        messages: {
            user_details: {
                required: "Please enter your details.",
                minlength: jQuery.validator.format("Please Enter at least {0} characters."),
            },
        },
        submitHandler: function(form) {
            var $form_group_loading = $(".form-group-loading");
            var $form_submit_wrap = $(".submit-btn-wrap");
            var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $("#settings-form :input").prop("disabled", true);
            loadingBefore($form_submit_wrap);
            if (formArray[1]) {
                user_avatar = formArray[1];
            }
            else {
                user_avatar = "";
            }
            $.ajax({
                url: "/api/users/" + $("#user-id").val() + "/",
                type: "PUT",
                datatype: "json",
                data:  {"user_gender": $("#id_user_gender option:selected").val(), "user_details": $("#user-details").val(), "user_avatar": user_avatar},
                beforeSend:function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                        xhr.setRequestHeader("X-CSRFToken", csrf_token);
                    } 
                },
                success: function(xhr) {
                    var $submit_btn_wrap = $(".submit-btn-wrap");
                    $submit_btn_wrap.empty();
                    var setting_upload_cover = $("<span />", {
                          "class": "setting-upload-cover btn btn-primary btn-file btn-block"
                      });
                    var upload_success = $("<span />", {
                          text: "Success",
                      });
                    setting_upload_cover.append(upload_success);
                    setting_upload_cover.appendTo($submit_btn_wrap).hide().fadeIn(500);
                },
                error: function(xhr, status, error) {
                    $form_submit_wrap.empty();
                    $("#settings-form :input").prop("disabled", false);
                    $(".form-server-error").empty();
                    var form_submit_button = $("<button />", {"class": "submit-btn btn btn-primary btn-block"});
                    var form_submit_button_span = $("<span />", {"class": "glyphicon glyphicon-ok"});
                    form_submit_button.append(form_submit_button_span);
                    $form_submit_wrap.append(form_submit_button);
                    var form_server_error = $("<div />", {
                          "class": "form-server-error"
                      });
                    if($('.form-server-error-p').length) {
                        console.log("already");    
                    } 
                    else{
                        $form_submit_wrap.before(form_server_error);
                    }
                    if (xhr.status >= 400 && xhr.status < 500) {
                        error_text = "Please check again your input.";
                    }
                    else {
                        error_text = "Please try again later";
                    }
                    $form_server_error_span = $("<span />", {"class": "pull-left form-server-error-span glyphicon glyphicon-exclamation-sign"});
                    $form_server_error_p = $("<p />", {"class": "form-server-error-p", text: "Please check again your input."});
                    $form_server_error_span.appendTo(form_server_error).hide().fadeIn();
                    $form_server_error_p.appendTo(form_server_error).hide().fadeIn();
                },
            });
        },
        success: function(label) {
        },
        highlight: function(element, errorClass) {
        }
    }); 
   
    $('.settings-img-outer-wrapper').on("click", function(){ 
        formData = new FormData();
        $.ajax({
            url: "/token",
            type: "GET",
            datatype: "json",
            data: {"type": 2},
            success: function(data) {
                formData.append("key", data["key"]);
                formData.append("token", data["token"]);
                formArray[1] = data["key"];
            },
        });
    });

    $('#avatar-input').on("change", function(){ 
        if (typeof (FileReader) != "undefined") {
            var image_holder = $(".settings-img-outer-wrapper");
            image_holder.empty();
            var reader = new FileReader();
            reader.onload = function (e) {
                $("<img />", {
                    "src": e.target.result,
                    "class": "unfinished-image",
                    "id": "avatar-upload-img"
                }).appendTo(image_holder);

            }
            //image_holder.show();
            reader.readAsDataURL($(this)[0].files[0]);
        } 
        else {
            console.log("This browser does not support FileReader.");
        }
        var file = this.files[0];
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
            beforeSend: function() {
            },
            success: function(data) {
                $(".progress").remove();
                $("#avatar-upload-img").removeClass("unfinished-image");
                $("#avatar-upload-img").addClass("finished-image");
            }
        });
    });
});


