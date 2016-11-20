$(document).ready(function(){
    $.validator.addMethod(
        "regex",
        function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Please check your email."
    );
    var validator = $("#signup_form").validate({
        rules: {
            email: {
                required: true,
                email: true,
                regex: /^[-a-z0-9~!$%^&*_=+}{\'?]+(\.[-a-z0-9~!$%^&*_=+}{\'?]+)*@([a-z0-9_][-a-z0-9_]*(\.[-a-z0-9_]+)*\.(aero|arpa|biz|com|coop|edu|gov|info|int|mil|museum|name|net|org|pro|travel|mobi|[a-z][a-z])|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,5})?$/i,   
                minlength: 7,
                remote: {
                    url: "/email/",
                    type: "post",
                    data: {
                        email: function() {
                        return $( "#email_signup" ).val();
                        }
                    }
                }
            },
            user_name: {
                required: true,
                minlength: 6,
                remote: {
                    url: "/checkuser/",
                    type: "post",
                    data: {
                        user_name: function() {
                        return $( "#username_signup" ).val();
                        }
                    }
                }
            },
            password: {
                required: true,
                minlength: 8
            },
        },
        messages: {
            user_name: {
                required: "Please enter your username.",
                minlength: jQuery.validator.format("Please Enter at least {0} characters."),
                remote: "This username had already been registered."
            },
            password: {
                required: "Please enter your password.",
                minlength: jQuery.validator.format("Please Enter at least {0} characters.")
            },
            email: {
                required: "Please enter a valid email address.",
                minlength: "Please enter a valid email address.",
                remote: "This email had already been registered."
            },
        },
        submitHandler: function(form) {
            $("#signup_form :input").prop("disabled", true);
            loadingBefore($(".submit-btn-wrap"));
            //var $form_group_loading = $(".form-group-loading");
            //var $form_submit_wrap = $(".submit-btn-wrap");
            //$form_submit_wrap.empty()
            //var form_outer_loading = $("<div />", {
            //              "class": "loading-center",
            //          });
            //var form_loading = $("<div />", {
            //              "class": "la-ball-clip-rotate la-sm",
            //          });
            //var form_inner_loading = $("<div />");
            //form_loading.append(form_inner_loading);
            //form_outer_loading.append(form_loading);
            //$form_submit_wrap.append(form_outer_loading);
            var user_name = $("#username_signup").val();
            user_name = user_name.replace(/\s+/g, '-');
            $.ajax({
                url: "/api/users/",
                type: "POST",
                datatype: "json",
                data:  {"email": $("#email_signup").val(), "user_name": user_name, "password": $("#password_signup").val()},
                beforeSend:function() {},
                success: function(xhr) {
                    window.location.replace("/");
                },
                error: function(xhr, status, error) {
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
                    if($('.form-server-error').length) {
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
            $(element).parent().next().find("." + errorClass).removeClass("checked");
        }
    });
});


