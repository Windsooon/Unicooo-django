$(document).ready(function(){
    $('.ball-scale div').show();
    $('.carousel-img').on('load', function(){
      $('.ball-scale div').hide();
    });
    var page = 1;
    var data = {"act_type": 2, "page": page};
    var scrollTimeout;
    var $container = $(".activity-container").masonry({
        itemSelector: '.act-outer-container',
        transitionDuration: '0.3s',
        hiddenStyle: { opacity: 0 },
        visibleStyle: { opacity: 1 }
    });
    get_act_list(data, $container)
});
