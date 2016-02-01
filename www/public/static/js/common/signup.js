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
            csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $("#signup_form :input").prop("disabled", true);
            $(".form-group-loading").empty();
            var form_outer_loading = $("<div />", {
                          "class": "loading-center",
                      });
            var form_loading = $("<div />", {
                          "class": "la-ball-clip-rotate la-sm",
                      });
            var form_inner_loading = $("<div />");
            form_loading.append(form_inner_loading);
            form_outer_loading.append(form_loading);
            $(".form-group-loading").append(form_outer_loading);
            console.log("submit");
            $.ajax({
                url: "/api/users/",
                type: "POST",
                datatype: "json",
                data:  {"csrfmiddlewaretoken": csrf_token},
                beforeSend:function() {},
                success: function(xhr) {
                    console.log(xhr.status);
                },
                error: function(xhr) {
                    console.log(xhr.status);
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


