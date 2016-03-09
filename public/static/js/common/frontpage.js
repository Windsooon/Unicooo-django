function imgError(image) {
    image.onerror = "";
    image.src = "../../static/img/error.png";
    return true;
}

$(document).ready(function(){
    $('.ball-scale div').show();
    $('.carousel-img').on('load', function(){
      $('.ball-scale div').hide();
    });
    
    if($(window).width() <= 767) {
        $(".thumbnail img").each(function() {
            $(this).attr("src", $(this).attr("src").replace("actCoverInterS", "actCoverInterB"));
        });
    }
});
