$(document).ready(function(){
    var $container = $("#posts-container");
    $container.imagesLoaded(function(){
        $container.masonry({
            itemSelector: ".post-container",
            gutterWidth: 20,
        });
    });
});
