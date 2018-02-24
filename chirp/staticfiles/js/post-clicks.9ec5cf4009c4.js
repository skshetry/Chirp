$(".like-click").click(function(event){
    event.preventDefault();
    var clicked = $(this);
    var like_count = parseInt($(this, '.like-count').text());
    if($(clicked).hasClass('btn-danger') == false){
        $(clicked).find('.like-count').text(++like_count);
    }
    else{
        $(clicked).find('.like-count').text(--like_count);
    }
    $(this).toggleClass('btn-danger');
    $(".like-click").blur(); 
    $.ajax({
        url: $(this).attr('href'),
        success: function(response){
            if(response.done == true){
                $(clicked).find('.like-count').text(response.likes_count);
                if($(this).hasClass('btn-danger') != false){
                    $(this).toggleClass('btn-danger');
                }
        }
        else if(response.done == false){
            $(clicked).find('.like-count').text(response.likes_count);
            if($(this).hasClass('btn-danger') == false){
                $(this).toggleClass('btn-danger');
            }
        }
    }
    });
});

$(".normal-share-click").click(function(event){
    event.preventDefault();
    var clicked = $(this);
    var like_count = parseInt($(share_count_btn, '.like-count').text());
    if($(clicked).hasClass('btn-danger') == false){
        $(clicked).find('.like-count').text(++like_count);
    }
    else{
        $(clicked).find('.like-count').text(--like_count);
    }
    var share_count_btn = $(this).closest('.dropdown-menu').siblings();
    share_count_btn.toggleClass('btn-danger');
    $(share_count_btn).blur(); 
    $.ajax({
        url: $(this).attr('href'),
        success: function(response){
            if(response.done == true && !isNaN(like_count)){
                $(share_count_btn).find('.like-count').text(response.shares_count);
                if($(share_count_btn).hasClass('btn-danger') != false){
                    $(share_count_btn).addClass('btn-danger');
                }
        }
        else if(response.done == false && !isNaN(like_count)){
            $(share_count_btn).find('.like-count').text(response.shares_count);
            if($(share_count_btn).hasClass('btn-danger') == false){
                $(share_count_btn).removeClass('btn-danger');
            }
        }
    }
    });
});

$('.share-click').click(function(event){
    event.preventDefault();
    var clicked = $(this);
    var cloned_post = $(this).closest('.media').clone();
    var share_post_id = $(this).closest('.media').attr('postid');
    $('.share-form').html(cloned_post);
    $('#share-post-input-id').val(share_post_id);
    $('#addmedia').hide();
    $(".like-click").blur(); 
    $('.media-forms').hide();
    $('.dropdown-menu').toggle();
    $('#postAddModal').modal('show');
});

$('.reply-click').click(function(event){
    event.preventDefault();
    var clicked = $(this);
    var cloned_post = $(this).closest('.media').clone();
    var reply_post_id = $(this).closest('.media').attr('postid');
    $('.reply-form').html(cloned_post);
    $(".like-click").blur(); 
    $('#reply-post-input-id').val(reply_post_id);
    $('#postAddModal').modal('show');
});
$('#close-post-btn').click(function(event){
    // do post cleanup
    $('.share-form').html('');
    $('#share-post-input-id').val('');
    $('.reply-form').html('');
    $('#reply-post-input-id').val('');
    $('#addmedia').show();
    $('.media-forms').show();
});