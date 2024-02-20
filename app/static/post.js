$('.respondingTo').on('click', function(){
    $('.card.container').toggleClass('shorten-box');
    $(this).toggleClass('fa-arrow-up-short-wide fa-arrow-down-short-wide');
})