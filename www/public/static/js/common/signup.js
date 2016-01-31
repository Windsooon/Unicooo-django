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
        submitHandler: function() {
            $(".form-group-loading").empty();
            var form_loading = $("<div />", {
                          "class": "la-ball-clip-rotate la-sm",
                      });
            var form_inner_loading = $("<div />", {
                          "class": "loading-center",
                      });
            form_loading.append(form_inner_loading);
            $(".form-group-loading").append(form_loading);
            console.log("submit");
            //form.submit();
        },
        success: function(label) {
            // set &nbsp; as text for IE
            console.log("success");
            //label.html("&nbsp;").addClass("checked");
        },
        highlight: function(element, errorClass) {
            $(element).parent().next().find("." + errorClass).removeClass("checked");
        }
    });
});


