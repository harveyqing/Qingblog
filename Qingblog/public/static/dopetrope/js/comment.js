/**
 * @author Chine - Modified by Harvey
 */
var locked = false;

$(function(){

    $("#commentform").ajaxForm({
        beforeSubmit: checkComment,
        success: dealResponse
    });

    $("input#not-robot").click(function() {
        $(this).toggle().hide();
    });

    $('div.reply').live('click', function() {
        var userName = $.trim($(this).siblings('header').children('cite').text());
        var commentId = $.trim($(this).parents('li:first').attr('id'));
        var commentId = commentId.split('-')[1];

        $('form#commentform input[type=button]:last').val('取消对' + userName + '的回应').show();
        $('html, body').scrollTop($('#commentform').offset().top);
        $('#reply_to_comment_id').val(commentId);
    });

    $('form#commentform input[type=button]:last').click(function() {
        var $hideId = $('#reply_to_comment_id');
        var commentId = $hideId.val();
        $hideId.val('');
        $('input#name').val('');
        $('input#email').val('');
        $('input#site').val('');
        $('textarea#content').val('');
        $(this).hide();
        $('html, body').scrollTop($('#comment-'+commentId).offset().top);
    });
});

function block(msg) {
    $.blockUI({
        message: msg,
        css: {
            width: '350px',
            border: 'none',
            padding: '15px 5px',
            backgroundColor: '#000',
            '-webkit-border-radius': '3px',
            '-moz-border-radius': '3px',
            'border-radius': '3px',
            opacity: .6,
            color: '#fff' ,
            'font-weight': 'bold'
        }
    });
}

function checkComment(formData, $form, options) {
    if(locked) {
        return false;
    }

    for(item in formData) {
        var obj = formData[item];

        var name = obj.name;
        var value = obj.value;

        if(name == 'username' || name == 'email' || name == "content") {
            if(value == '' || typeof value == undefined) {
                block(commentTips['miss']);
                setTimeout($.unblockUI, 1500);
                return false;
            }

            if (name == 'email' && (null == value.trim().match(/^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/) )) {
                block(commentTips['email']);
                setTimeout($.unblockUI, 1500);
                return false;
            }
        }
    }

    if(!locked) {
        locked = true;
    }
}

function dealResponse(responseText, statusText) {
    if (responseText.status == "0") {
        block(commentTips['success']);
        $("section#comments").replaceWith(responseText.comments);
        $('#reply_to_comment_id').val('');
        if (responseText.inserted_id) {
            element = $('#comment-'+responseText.inserted_id)
            if (element.offset() !== undefined) {
                $('html, body').scrollTop(element.offset().top);
            } else {location.reload();}
        };
        $('input#name').val('');
        $('input#email').val('');
        $('input#site').val('');
        $('textarea#content').val('');
        $('form#commentform input[type=button]:last').hide();
        $.unblockUI();
    }

    if(locked) {
        locked = false;
    }
}
