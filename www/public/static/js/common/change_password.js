$(document).ready(function() {
   formArray = new Array();
   var csrftoken = getCookie('csrftoken');

   var validator = $("#change-password-form").validate({
        rules: {
            old_password: {
                required: true,
                remote: {
                    url: "/check_old_password/",
                    type: "POST",
                    data: {
                        old_password: function() {
                            return $("#id_old_password").val();
                        },
                        csrfmiddlewaretoken: csrftoken,
                    }
                }
            },
            new_password1: {
                required: true,
                equalTo: "#id_new_password2"
            },
            new_password2: {
                required: true,
                equalTo: "#id_new_password1"
            },
        },
        messages: {
            old_password: {
                required: "Please enter your old password.",
                remote: "Your old password is incorret",
            },
            new_password1: {
                required: "Please enter your new password.",
                equalTo: "Password doesn't match the confirmation"
            },
            new_password2: {
                required: "Please enter your new password again.",
                equalTo: "Password doesn't match the confirmation"
            },
        },
        submitHandler: function(form) {
            var $form_group_loading = $(".form-group-loading");
            var $form_submit_wrap = $(".submit-btn-wrap");
            var csrftoken = getCookie('csrftoken');
            $("#change-password-form :input").prop("disabled", true);
            loadingBefore($form_submit_wrap);

            $.ajax({
                url: "/password_reset/",
                type: "POST",
                datatype: "json",
                data:  {"new_password": $("#id_new_password1").val()},
                beforeSend:function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    } 
                },
                success: function(xhr) {
                    var $submit_btn_wrap = $(".submit-btn-wrap");
                    $submit_btn_wrap.empty();
                    var setting_upload_cover = $("<span />", {
                          "class": "setting-upload-cover btn btn-primary btn-file btn-block"
                      });
                    var upload_success = $("<span />", {
                          "class": "success-span",
                          text: "Success",
                      });
                    setting_upload_cover.append(upload_success);
                    setting_upload_cover.appendTo($submit_btn_wrap).hide().fadeIn(500);
                },
                error: function(xhr, status, error) {
                    $form_submit_wrap.empty();
                    $("#change-password-form :input").prop("disabled", false);
                    $(".form-server-error").empty();
                    var form_submit_button = $("<button />", {"class": "submit-btn btn btn-primary btn-block"});
                    var form_submit_button_span = $("<span />", {"class": "glyphicon glyphicon-ok"});
                    form_submit_button.append(form_submit_button_span);
                    $form_submit_wrap.append(form_submit_button);
                    var form_server_error = $("<div />", {
                          "class": "form-server-error"
                      });
                    if($('.form-server-error-p').length == 0) {
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
        },
    }); 
});
