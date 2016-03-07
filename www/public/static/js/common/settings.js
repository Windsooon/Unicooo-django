$(document).ready(function () {
    var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    console.log(csrf_token);
    $("#setting-btn").on("click", function() {
        $.ajax({
                url: "/api/users/22/",
                type: "PUT",
                datatype: "json",
                //data:  {csrfmiddlewaretoken: csrf_token, "user_gender": $("#id_user_gender option:selected").val(), "user_details": $("#user-details").val() },
                data:  {csrfmiddlewaretoken: csrf_token, "user_gender": $("#id_user_gender option:selected").val(), "user_details": $("#user-details").val() },
                beforeSend:function() {},
                success: function(xhr) {
                    window.location.replace("/");
                },
        });
    });
    
});

//$(document).ready(function() {
//   var validator = $("#settings-form").validate({
//        rules: {
//            user_details: {
//                required: true,
//                minlength: 10,
//            },
//        },
//        messages: {
//            user_details: {
//                required: "Please enter your details.",
//                minlength: jQuery.validator.format("Please Enter at least {0} characters."),
//            },
//        },
//        submitHandler: function(form) {
//            var $form_group_loading = $(".form-group-loading");
//            var $form_submit_wrap = $(".submit-btn-wrap");
//            var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
//            $("#settings-form :input").prop("disabled", true);
//            $form_submit_wrap.empty()
//            var form_outer_loading = $("<div />", {
//                          "class": "loading-center",
//                      });
//            var form_loading = $("<div />", {
//                          "class": "la-ball-clip-rotate la-sm",
//                      });
//            var form_inner_loading = $("<div />");
//            form_loading.append(form_inner_loading);
//            form_outer_loading.append(form_loading);
//            $form_submit_wrap.append(form_outer_loading);
//            $.ajax({
//                url: "/api/users/" + $("#user-id").val() + "/",
//                type: "PUT",
//                datatype: "json",
//                data:  {csrfmiddlewaretoken: csrf_token, "user_gender": $("#id_user_gender option:selected").val(), "user_details": $("#user-details").val() },
//                beforeSend:function() {},
//                success: function(xhr) {
//                    window.location.replace("/");
//                },
//                error: function(xhr, status, error) {
//                    $form_submit_wrap.empty();
//                    $("#settings-form :input").prop("disabled", false);
//                    $(".form-server-error").empty();
//                    var form_submit_button = $("<button />", {"class": "submit-btn btn btn-primary btn-block"});
//                    var form_submit_button_span = $("<span />", {"class": "glyphicon glyphicon-ok"});
//                    form_submit_button.append(form_submit_button_span);
//                    $form_submit_wrap.append(form_submit_button);
//                    var form_server_error = $("<div />", {
//                          "class": "form-server-error"
//                      });
//                    if($('.form-server-error-p').length) {
//                        console.log("already");    
//                    } 
//                    else{
//                        $form_submit_wrap.before(form_server_error);
//                    }
//                    if (xhr.status >= 400 && xhr.status < 500) {
//                        error_text = "Please check again your input.";
//                    }
//                    else {
//                        error_text = "Please try again later";
//                    }
//                    $form_server_error_span = $("<span />", {"class": "pull-left form-server-error-span glyphicon glyphicon-exclamation-sign"});
//                    $form_server_error_p = $("<p />", {"class": "form-server-error-p", text: "Please check again your input."});
//                    $form_server_error_span.appendTo(form_server_error).hide().fadeIn();
//                    $form_server_error_p.appendTo(form_server_error).hide().fadeIn();
//                },
//            });
//        },
//        success: function(label) {
//        },
//        highlight: function(element, errorClass) {
//        }
//    }); 
//});
