$(document).ready(function(){
    var $container = $('#act_grid');
    $container.imagesLoaded(function(){
        $container.masonry({
            itemSelector: '.act_item',
            gutterWidth: 20,
        });
    });
});
