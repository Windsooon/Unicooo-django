$(document).ready(function(){
    var $container = $('#posts-container').masonry();
    var formData = new FormData();
    var formArray = new Array();
    var imageUrl = "https://o2ocy30id.qnssl.com/";
    var imageStyle = "-actCoverInterS";
    $post_cover_span = $(".upload-cover");
    $('#post-upload-image').on("click", function(){ 
        formData = new FormData();
        formArrar = new Array();
        $.ajax({
            url: "/token",
            type: "GET",
            datatype: "json",
            data: {"type": 1},
            success: function(data) {
                formData.append("token", data["token"]);
                formData.append("key", data["key"]);
                formArray[0] = data["token"];
                formArray[1] = data["key"];
            },
        });
    });

    $("#post-upload-image").on('change', function () {
        if (typeof (FileReader) != "undefined") {
            var image_holder = $(".post-upload-div");
            image_holder.empty();
            var reader = new FileReader();
            reader.onload = function (e) {
                $("<img />", {
                    "src": e.target.result,
                    "class": "post-unfinished-image"
                }).appendTo(image_holder);

            }
            image_holder.show();
            reader.readAsDataURL($(this)[0].files[0]);
        } 
        else {
            console.log("This browser does not support FileReader.");
        }
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
               $post_cover_span.empty(); 
               var post_outer_loading = $("<div />", {
                          "class": "",
                      });
               var post_loading = $("<div />", {
                          "class": "la-ball-clip-rotate la-sm",
                      });
               var post_inner_loading = $("<div />");
               post_loading.append(post_inner_loading);
               post_outer_loading.append(post_loading);
               $post_cover_span.append(post_outer_loading);
            },
            error: function(data) {
               console.log("error");
               $post_cover_span.empty(); 
               $post_cover_span.html("Please check your internet conection.");
               var upload_failed = $("<input>").attr({
                           "class": "cropit-image-input", 
                           type: "file",
                           id: "act-cover-image",
                       });                  
               upload_failed.appendTo($post_cover_span).hide().fadeIn(500);
            },
            success: function(data) {
               console.log(formArray[1]);
               console.log(formArray[2]);
               console.log(formArray[3]);
               console.log(window.CSRF_TOKEN);
               $(".post-upload-div img").removeClass("post-unfinished-image");
               $(".post-upload-div img").addClass("post-finished-image");
               var post_a = $("<a />", {
                          "class": "",
                          href: "#post_details",
                          "data-toggle": "modal",
                          "data-target": "#post-details",
                      });
               var post_image = $("<img />", {
                          src: imageUrl + data["key"],
                      });
               var post_div = $("<div />", {
                          "class": "post-container"
                      });
               post_a.append(post_image)
               post_div.append(post_a);
               $container.prepend(post_div)
               $container.imagesLoaded(function() {
                   $container.masonry('prepended', post_div);
               });
               //$container.masonry('prepended', $items);
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
               $post_cover_span.empty(); 
               var upload_success = $("<span />", {
                          text: "Success",
                      });
               upload_success.appendTo($post_cover_span).hide().fadeIn(500);
               $("#act_title").after(upload_key);
            },
        });
    });
});
