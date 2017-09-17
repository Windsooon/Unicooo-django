$(document).ready(function(){
    $.validator.addMethod(
        "regex",
        function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Email format is invalid."
    );
    $.validator.addMethod(
        "regex_name",
        function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Username may only contain alphanumeric characters."
    );
    var validator = $("#signup_form").validate({
        rules: {
            email: {
                required: true,
                email: true,
                regex: /^[-a-z0-9~!$%^&*_=+}{\'?]+(\.[-a-z0-9~!$%^&*_=+}{\'?]+)*@([a-z0-9_][-a-z0-9_]*(\.[-a-z0-9_]+)*\.(aero|arpa|biz|com|coop|edu|gov|info|int|mil|museum|name|net|org|pro|travel|mobi|[a-z][a-z])|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,5})?$/i,   
                minlength: 7,
                remote: {
                    url: "/checkemail/",
                    type: "get",
                    data: {
                        email: function() {
                            return $("#email_signup").val();
                        }
                    }
                }
            },
            user_name: {
                required: true,
                minlength: 6,
                maxlength: 30,
                regex_name: /^((?!'|"|<|>).)*$/,
                remote: {
                    url: "/checkuser/",
                    type: "get",
                    data: {
                        user_name: function() {
                        return $("#username_signup").val();
                        }
                    }
                }
            },
            password: {
                required: true,
                minlength: 8,
                maxlength: 40,
            },
        },
        messages: {
            user_name: {
                required: "Please enter your username.",
                minlength: jQuery.validator.format("Please Enter at least {0} characters."),
                maxlength: jQuery.validator.format("Username under 30 characters will be nice."),
                remote: "This username had already been registered."
            },
            password: {
                required: "Please enter your password.",
                minlength: jQuery.validator.format("Please Enter at least {0} characters."),
                maxlength: jQuery.validator.format("Please Enter up to  {0} characters."),
            },
            email: {
                required: "Please enter a valid email address.",
                minlength: "Please enter a valid email address.",
                remote: "This email had already been registered."
            },
        },
        submitHandler: function(form) {
            var csrftoken = getCookie('csrftoken');
            $("#signup_form :input").prop("disabled", true);
            loadingBefore($(".submit-btn-wrap"));
            var user_name = $("#username_signup").val();
            user_name = user_name.replace(/\s+/g, '-');
            $.ajax({
                url: "/api/users/",
                type: "POST",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken)
                },
                datatype: "json",
                data:  {
                    csrfmiddlewaretoken: csrftoken,
                    "email": $("#email_signup").val(), "user_name": user_name, "password": $("#password_signup").val()},
                beforeSend:function() {},
                success: function(xhr) {
                    window.location.replace("/");
                },
                error: function(xhr, status, error) {
                    $form_submit_wrap = $(".submit-btn-wrap");
                    $form_submit_wrap.empty();
                    $("#signup_form :input").prop("disabled", false);
                    $(".form-server-error").empty();
                    var form_submit_button = $("<button />", {"class": "submit-btn btn btn-primary btn-block"});
                    var form_submit_button_span = $("<span />", {"class": "glyphicon glyphicon-ok"});
                    form_submit_button.append(form_submit_button_span);
                    $form_submit_wrap.append(form_submit_button);
                    var form_server_error = $("<div />", {
                          "class": "form-server-error"
                    });
                    if($('.form-server-error').length == 0) {
                        $form_submit_wrap.before(form_server_error);
                    }
                    if (xhr.status >= 400 && xhr.status < 500) {
                        if (xhr.responseText.indexOf("exists") !== -1) {
                           var error_text = "Username or Email already Exists, Please Login.";
                        }
                        else {
                           var error_text = "Please try again later.";
                        }
                    }
                    else {
                        var error_text = "Server Error.";
                    }
                    if ($(".form-server-error-p").length > 0) {
                        $(".form-server-error-p").remove();
                    }
                    $form_server_error_span = $("<span />", {"class": "pull-left form-server-error-span glyphicon glyphicon-exclamation-sign"});
                    $form_server_error_p = $("<p />", {"class": "form-server-error-p", text: error_text});
                    $form_server_error_span.appendTo(form_server_error).hide().fadeIn();
                    $form_server_error_p.appendTo(form_server_error).hide().fadeIn();
                },
            });
        },
        success: function(label) {
        },
        highlight: function(element, errorClass) {
            $(element).parent().next().find("." + errorClass).removeClass("checked");
        }
    });
});


