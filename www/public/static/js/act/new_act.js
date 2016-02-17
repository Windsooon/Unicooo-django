$(document).ready(function(){
    var formData = new FormData();
    $act_cover_span = $("#act-cover-span");
    $('#act-cover-image').on("click", function(){ 
        formData = new FormData();
        $.ajax({
            url: "/token",
            type: "GET",
            datatype: "json",
            success: function(data) {
                formData.append("token", data["token"]);
                formData.append("key", data["key"]);
            },
        });
    });

    $('#act-cover-image').on("change", function(){ 
        var file = this.files[0];
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
               $act_cover_span.empty(); 
            },
            success: function(data) {
               console.log("success");
               $("#act-cover-btn").prop("disabled", false);
               $act_cover_span.empty(); 
               var upload_success = $("<span />", {
                          "class": "",
                          text: "Success",
                      });
               upload_success.appendTo($act_cover_span).hide().fadeIn(500);
            },
        });
    });

    function uploadFile() {
        
    }
});
