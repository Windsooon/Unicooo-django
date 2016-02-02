$(document).ready(function(){

    var validator = $("#signup_form").validate({
        rules: {
            email: {
                required: true,
                email: true,
                minlength: 7,
            },
            user_name: {
                required: true,
                minlength: 6,
            },
            password: {
                required: true,
                minlength: 8
            },
        },
        messages: {
            user_name: {
                required: "Please enter your username",
                minlength: jQuery.validator.format("Please Enter at least {0} characters"),
            },
            password: {
                required: "Please enter your password",
                minlength: jQuery.validator.format("Please Enter at least {0} characters")
            },
            email: {
                required: "Please enter a valid email address",
                minlength: "Please enter a valid email address",
            },
        },
        submitHandler: function(form) {
            var $form_group_loading = $(".form-group-loading");
            var $form_submit_wrap = $(".submit-btn-wrap");
            //csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $("#signup_form :input").prop("disabled", true);
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
            console.log("submit");
            $.ajax({
                url: "/api/users/",
                type: "POST",
                datatype: "json",
                data:  {"email": $("#email_signup").val()},
                beforeSend:function() {},
                success: function(xhr) {
                    console.log(xhr.status);
                },
                error: function(xhr, status, error) {
                    $form_submit_wrap.empty();
                    $(".form-server-error").empty();
                    var form_submit_button = $("<button />", {"class": "submit-btn btn btn-primary btn-block"});
                    var form_submit_button_span = $("<span />", {"class": "glyphicon glyphicon-ok"});
                    form_submit_button.append(form_submit_button_span);
                    $form_submit_wrap.append(form_submit_button);
                    var form_server_error = $("<div />", {
                          "class": "form-server-error"
                      });
                    $form_submit_wrap.before(form_server_error);
                    if (xhr.status == 400) {
                        $form_server_error_span = $("<span />", {"class": "pull-left form-server-error-span glyphicon glyphicon-exclamation-sign"});
                        $form_server_error_p = $("<p />", {"class": "form-server-error-p", text: "Please check again your input."});
                        $form_server_error_span.appendTo(form_server_error).hide().fadeIn();
                        $form_server_error_p.appendTo(form_server_error).hide().fadeIn();
                    }
                },
            });
        },
        success: function(label) {
            label.parent().parent().addClass("has-success");
        },
        highlight: function(element, errorClass) {
            $(element).parent().next().find("." + errorClass).removeClass("checked");
        }
    });
});


