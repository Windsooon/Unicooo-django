$(document).ready(function(){
    $.validator.addMethod(
        "regex",
        function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Please check your email address."
    );
    var validator = $("#login_form").validate({
        rules: {
            email: {
                required: true,
                email: true,
                regex: /^[-a-z0-9~!$%^&*_=+}{\'?]+(\.[-a-z0-9~!$%^&*_=+}{\'?]+)*@([a-z0-9_][-a-z0-9_]*(\.[-a-z0-9_]+)*\.(aero|arpa|biz|com|coop|edu|gov|info|int|mil|museum|name|net|org|pro|travel|mobi|[a-z][a-z])|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,5})?$/i,   
                minlength: 7,
            },
            password: {
                required: true,
                minlength: 8
            },
        },
        messages: {
            email: {
                required: "Please enter a valid email address.",
                minlength: "Please enter a valid email address.",
            },
            password: {
                required: "Please enter your password.",
                minlength: jQuery.validator.format("Please Enter at least {0} characters.")
            },
        },
        submitHandler: function(form) {
            $("#login_form :input").prop("disabled", true);
            loadingBefore($(".submit-btn-wrap"));
            csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax({
                url: "/login/",
                type: "POST",
                datatype: "json",
                data:  {csrfmiddlewaretoken: csrf_token, "email": $("#email_login").val(),"password": $("#password_login").val()},
                beforeSend:function() {},
                success: function(xhr) {
                    var current_url = window.location.href; 
                    var location = current_url.split("next=", 2);
                    window.location.replace(location[1]);
                },
                error: function(xhr, status, error) {
                    $form_submit_wrap = $(".submit-btn-wrap");
                    $form_submit_wrap.empty();
                    $("#login_form :input").prop("disabled", false);
                    $(".form-server-error").remove();
                    var form_submit_button = $("<button />", {"class": "submit-btn btn btn-primary btn-block"});
                    var form_submit_button_span = $("<span />", {"class": "glyphicon glyphicon-ok"});
                    form_submit_button.append(form_submit_button_span);
                    $form_submit_wrap.append(form_submit_button);
                    var form_server_error = $("<div />", {
                          "class": "form-server-error"
                      });
                    $form_submit_wrap.before(form_server_error);
                    if (xhr.status >= 400 && xhr.status < 500) {
                        if (xhr.responseText == 10002) {
                            error_text = "Email or password incorrect.";
                        }
                        else {
                            error_text = "Please check again your input.";
                        }
                    }
                    else {
                        error_text = "Something wrong with our server!";
                    }
                    $form_server_error_span = $("<span />", {"class": "pull-left form-server-error-span glyphicon glyphicon-exclamation-sign"});
                    $form_server_error_p = $("<p />", {"class": "form-server-error-p", text: error_text});
                    $form_server_error_span.appendTo(form_server_error).hide().fadeIn();
                    $form_server_error_p.appendTo(form_server_error).hide().fadeIn();
                },
            });
        },
        success: function(label) {
            //label.parent().parent().addClass("has-success");
        },
        highlight: function(element, errorClass) {
            $(element).parent().next().find("." + errorClass).removeClass("checked");
        }
    });
});



