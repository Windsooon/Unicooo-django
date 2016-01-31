$(document).ready(function(){
    var validator = $("#signup_form").validate({
			rules: {
                email: {
					required: true,
					email: true,
					minlength: 8,
					remote: "emails.action"
				},
				user_name: {
					required: true,
					minlength: 6,
					remote: "users.action"
				},
				password: {
					required: true,
					minlength: 5
				},
			},
			messages: {
				username: {
					required: "Enter a username",
					minlength: jQuery.validator.format("Enter at least {0} characters"),
					remote: jQuery.validator.format("{0} is already in use")
				},
				password: {
					required: "Provide a password",
					minlength: jQuery.validator.format("Enter at least {0} characters")
				},
				email: {
					required: "Please enter a valid email address",
					minlength: "Please enter a valid email address",
					remote: jQuery.validator.format("{0} is already in use")
				},
			},
			// the errorPlacement has to take the table layout into account
			errorPlacement: function(error, element) {
				if (element.is(":radio"))
					error.appendTo(element.parent().next().next());
				else if (element.is(":checkbox"))
					error.appendTo(element.next());
				else
					error.appendTo(element.parent().next());
			},
			// specifying a submitHandler prevents the default submit, good for the demo
			submitHandler: function() {
				alert("submitted!");
			},
			// set this class to error-labels to indicate valid fields
			success: function(label) {
				// set &nbsp; as text for IE
				label.html("&nbsp;").addClass("checked");
			},
			highlight: function(element, errorClass) {
				$(element).parent().next().find("." + errorClass).removeClass("checked");
			}
		});
});

