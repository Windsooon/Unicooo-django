$(document).ready(function(){
    $('.modal').on('hidden.bs.modal', function (e) {
        if($('.modal').hasClass('in')) {
            $('body').addClass('modal-open');
        }    
    });
    var $container = $('#posts-container').masonry();
    var formData = new FormData();
    var formArray = new Array();
    var imageStyle = "-actCoverBig";
    var xhrAjax = null;
    $post_cover_span = $(".upload-cover");

    $("body").on("click", ".add-url-btn", function() {
        $(".post-form-url").show();
    });

    //显示剩余输入字数
    $(document).on("keyup", ".post-form-text", function(){
        var $post_length = $(".post-form-length");
        //length未必存在
        if ($(".post-form-text").val().length) {
            var currrent_length = $(".post-form-text").val().length;   
            if (currrent_length >= 1 && currrent_length <= 60) {
                $post_length.text(60-currrent_length);
                if ($(".add-post-btn").is(":disabled") && post_upload_status) {
                    $(".add-post-btn").prop('disabled', false);
                }
            }
            else {
                $post_length.text("beyond 60 char");
                $post_length.css("color","#3f51b5");
                $(".add-post-btn").prop("disabled", true);
            }
        }
        else {
            $post_length.text(60);
        }
    }); 
    
    //click "UPLOAD IMAGE" button
    formData = new FormData();
    formArrar = new Array();
    $.ajax({
        url: "/token/",
        type: "GET",
        datatype: "json",
        data: {"type": 1},
        success: function(data) {
            formData.append("token", data["token"]);
            formData.append("key", data["key"]);
            formArray[1] = data["key"];
        },
    });
    
    //when post image change
    $(document).on("change", ".post-upload-image", function(){
        if (typeof (FileReader) != "undefined") {
            var upload_file = $(this)[0].files[0];
            switch (upload_file.type)
            {
            // if file is image
            case "image/jpeg":
            case "image/png":
            case "image/gif":
            case "image/jpg":
            case "image/bmp":
            case "image/tiff":
                var image_holder = $(".post-upload-div");
                image_holder.empty();
                var reader = new FileReader();
                reader.onload = function (e) {
                    var img = new Image;
                    img.onload = function() {
                        formArray[2] = img.width;
                        formArray[3] = img.height;
                        formArray[5] = 0;
                    };
                    img.src = reader.result;
                    $("<img />", {
                        "src": e.target.result,
                        "class": "unfinished-image",
                        "class": "post-upload-img"
                    }).appendTo(image_holder);
                }
                image_holder.show();
                reader.readAsDataURL($(this)[0].files[0]);
                break;
            //if file is audio
            case "audio/mp3":
            case "audio/mpeg":
            case "audio/ogg":
            case "audio/x-ogg":
            case "audio/wav":
            case "audio/x-m4a":
            case "audio/x-wav":
            case "audio/x-ms-wma":
            case "audio/x-mpegurl":
            case "audio/mod":
                var image_holder = $(".post-upload-div");
                image_holder.empty();
                var reader = new FileReader();
                reader.onload = function (e) {
                        formArray[2] = 350;
                        formArray[3] = 400;
                        formArray[5] = 1;
                    };
                    $("<img />", {
                        "src": "https://o3e6g3hdp.qnssl.com/audio.jpg",
                        "class": "unfinished-image",
                        "class": "post-upload-img"
                    }).appendTo(image_holder);
                image_holder.show();
                reader.readAsDataURL($(this)[0].files[0]);
                break;
            default: 
                //alert("This file has't been supported"); 
                return;
            }
        } 
        else {
            alert("This browser does not support FileReader.");
        }
        var file = this.files[0];
        formData.append("file", file);
        $(".post-form-text").prop("disabled", false);
        // if already had ajax requests at first
        if( xhrAjax != null ) {
                xhrAjax.abort();
                xhrAjax = null;
        }

        $("#post-upload").on('hidden.bs.modal', function(e) { 
                xhrAjax.abort();
        });
        
        xhrAjax = $.ajax({
            xhr: function() {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", function(evt) {
                  if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    percentComplete = parseInt(percentComplete * 100);
                    $(".progress-bar").css("width", percentComplete + "%")
                  }
                }, false);
                return xhr;
            },
            url: "https://up.qbox.me/",
            type: "POST",
            data: formData,
            datatype: "json",
            cache: false,
            processData: false, 
            contentType: false,
            beforeSend:function(){
                loadingBefore($(".upload-cover"));
            },
            error: function(xhr, status, error) {
                if (xhr.status >= 400 && xhr.status < 500) {
                        alert(xhr.responseText);
                        error_text = "Please check again your input.";
                }
                else {
                    error_text = "Please try again later.";
                }
                $post_cover_span.empty(); 
                $post_cover_span.html(error_text);
                var upload_failed = $("<input>").attr({
                           "class": "cropit-image-input", 
                           type: "file",
                           id: "act-cover-image",
                       });                  
                upload_failed.appendTo($post_cover_span).hide().fadeIn(500);
            },
            success: function(data) {
                $(".post-upload-div img").attr("class", "post-upload-img");
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
                loadingAfter($(".upload-cover"), 1);
                $("#act_title").after(upload_key);
            },
            complete: function() {
                post_upload_status = true;
                $(".post-upload-div img").removeClass("unfinished-image");
                $(".post-upload-div img").addClass("finished-image");
                var post_length = $(".post-form-text").val().length + 1;
                if (post_length >= 2 && post_length <= 60 && $('.add-post-btn').is(":disabled")) {
                    $('.add-post-btn').prop('disabled', false);
                }
            },
        });
    });

    $(document).on("submit", ".post-content-upload", function(e){
        e.preventDefault();
        var re = new RegExp("^((?!\'|\"|<|>).)*$");
        var post_form_url = $(".post-form-url").val();
        if($(".post-form-url").css("display") != "none" && !validateUrl(post_form_url)) {
            alert("Url not valid."); 
            return false;
        }
        $activity_input = $(".activity-details-content input");
        var post_content = $(".post-form-text").val();
        if (!post_content.match(re)) {
            alert("Post content may only contain alphanumeric characters."); 
            return false;
        }
        var post_url = $(".post-form-url").val();
        var base64_src = $(".post-upload-img").attr("src");
        var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        formArray[4] = $activity_input.eq(0).val();
        formArray[6] = post_content
        if (!startsWith(post_url, 'http') && !startsWith(post_url, 'https'))  {
            post_url = "http://" + post_url; 
        }
        $.ajax({
            url: "/api/posts/",
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrf_token,
                "post_thumb_url": formArray[1],
                "post_thumb_width": formArray[2], "post_thumb_height": formArray[3], "nsfw": 0, "post_mime_types": formArray[5], "act": formArray[4], "post_content": formArray[6], "post_url": post_url}, 
            datatype: "json",
            beforeSend: function(){
                $(".post-form-text").prop("disabled", true);
            },
            success: function(data) {
                var date = data["post_create_time"].split("T", 1);
                var post_a = $("<a />", {
                            "class": "post-thumb-a",
                            href: "#post_details",
                            "data-toggle": "modal",
                            "data-target": "#post-details",
                        });
                 if (data["post_mime_types"] == 0) {
                     var post_image = $("<img />", {
                            "class": "post-container-img",
                            src: base64_src,
                        });
                      post_a.append(post_image)
                 }
                 else if (data["post_mime_types"] == 1) {
                     var audio_div_wrapper = $("<div />", {
                            "class": "audio-div-wrapper",
                        });
                     var audio_div = $("<div />", {
                            "class": "audio-div",
                        });
                     var audio_div_p = $("<p />", {
                            "class": "audio-div-p",
                            text: data["post_content"],
                        });
                     var audio_fadeout = $("<div />", {
                            "class": "act-fadeout",
                        });
                     var audio_tag = $("<audio />", {
                            "class": "audio-div-audio",
                            src: httpsUrl + data["post_thumb_url"],

                            "controls": "controls",
                            "preload": "auto",
                        });
                     audio_div.append(audio_div_p);
                     audio_div_wrapper.append(audio_div);
                     post_a.append(audio_div_wrapper);
                     post_a.append(audio_fadeout);
                     post_a.append(audio_tag);
                 }
                 var post_div_wrapper = $("<div />", {
                            "class": "post-container-col"
                        });
                 var post_div = $("<div />", {
                            "class": "post-container col-xs-12 col-sm-6 col-md-6 col-lg-4",
                            id: "post-" + data["id"]
                        });
                 var post_border = $("<div />", {
                            "class": "post-border"
                        });
                 var post_title = $("<div />", {
                            "class": "post-title"
                        });
                 var post_user = $("<p />", {
                            "class": "post-user",
                            text: data["post_user"]["user_name"]
                        });
                 var post_posttime = $("<div />", {
                            "class": "post-posttime"
                        });
                 var post_posttime_p = $("<p />", {
                            "class": "post-posttime-p",
                            text: date,
                        });
                 var post_content = $("<div />", {
                            "class": "post-content",
                        });
                 var post_content_p = $("<p />", {
                            "class": "post-content-p",
                            text: data["post_content"],
                        });
                 var post_footer = $("<div />", {
                            "class": "post-footer clearfix"
                        });
                 var post_like = $("<span />", {
                            "class": "post-like glyphicon glyphicon-heart pull-right"
                        });
                 var post_comment = $("<span />", {
                            "class": "post-comment glyphicon glyphicon-comment pull-right"
                        });

                 post_title.append(post_user);
                 post_posttime.append(post_posttime_p);
                 post_border.append(post_title);
                 post_border.append(post_posttime);
                 //
                 post_footer.append(post_like);
                 post_footer.append(post_comment);
                 //
                 post_content.append(post_content_p);
                 post_div_wrapper.append(post_a);
                 post_div_wrapper.append(post_border);
                 post_div_wrapper.append(post_content);
                 post_div_wrapper.append(post_footer);
                 post_div.append(post_div_wrapper);
                 $container.prepend(post_div)
                 $container.imagesLoaded(function() {
                     $container.masonry('prepended', post_div);
                 });
                 $(".post-thumb-a:first").attr({"data-post-id": data["id"]});
                 $("#post-upload").modal("hide");
            }, 
            error: function(data) {
            },
         });
      });
  });


