$(document).ready(function(){
    var formData = new FormData();
    var formArray = new Array();
    $act_cover_span = $("#act-cover-span");
    $('#act-cover-image').on("click", function(){ 
        formData = new FormData();
        formArrar = new Array();
        $.ajax({
            url: "/token",
            type: "GET",
            datatype: "json",
            success: function(data) {
                formData.append("token", data["token"]);
                formData.append("key", data["key"]);
                formArray[0] = data["token"];
                formArray[1] = data["key"];
            },
        });
    });

    $('#act-cover-image').on("change", function(){ 
        var file = this.files[0];
        var fr = new FileReader;
        fr.onload = function() { //file is loaded
            var img = new Image;
            img.onload = function() {
                formArray[2] = img.height;
                formArray[3] = img.width;
            };
            img.src = fr.result; //is the data URL because called with readAsDataURL
        };
        fr.readAsDataURL(file);
        formData.append("file", file);
        $.ajax({
            url: "http://upload.qiniu.com",
            type: "POST",
            data: formData,
            datatype: "json",
            cache: false,
            processData: false, 
            contentType: false,
            beforeSend:function(){
               $act_cover_span.empty(); 
               $("#act-cover-btn").prop("disabled", true);
               var act_outer_loading = $("<div />", {
                          "class": "",
                      });
               var act_loading = $("<div />", {
                          "class": "la-ball-clip-rotate la-sm",
                      });
               var act_inner_loading = $("<div />");
               act_loading.append(act_inner_loading);
               act_outer_loading.append(act_loading);
               $act_cover_span.append(act_outer_loading);
            },
            error: function(data) {
               console.log("error");
               $act_cover_span.empty(); 
               $act_cover_span.html("Please check your internet conection.");
               var upload_failed = $("<input>").attr({
                           "class": "cropit-image-input", 
                           type: "file",
                           id: "act-cover-image",
                       });                  
               upload_failed.appendTo($act_cover_span).hide().fadeIn(500);
            },
            success: function(data) {
               var upload_key = $("<input>").attr({
                           value: formArray[1],
                           name: "upload_key",
                           type: "hidden",
                           id: "upload_key",
                       });    
               var upload_image_width = $("<input>").attr({
                           value: formArray[2],
                           name: "image_width",
                           type: "hidden",
                           id: "image_width",
                       }); 
                var upload_image_height = $("<input>").attr({
                           value: formArray[3],
                           name: "image_height",
                           type: "hidden",
                           id: "image_height",
                       }); 
               $("#act-cover-btn").prop("disabled", false);
               $act_cover_span.empty(); 
               var upload_success = $("<span />", {
                          text: "Success",
                      });
               upload_success.appendTo($act_cover_span).hide().fadeIn(500);
               $("#act_title").after(upload_key);
               $("#act_title").after(upload_image_width);
               $("#act_title").after(upload_image_height);
            },
        });
    });
});
