var $form = $('#form');
var flag = true;
$('.comment-text a').click(function(){
    $form.hide();
    $('.comment-reply').text('Ответить');
    if(!$(this).hasClass('active')){
        $(this).text('Отмена').addClass('active');
        var $comment = $(this).parent();
        $form.find('#parent_id').val($comment.attr('id'));
        $comment .append($('#form').show());
    }
    else{
        $('.comment-text a').removeClass('active');
        $('.comment-respond').append($('#form').show());
    }
});