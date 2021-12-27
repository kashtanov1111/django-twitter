var followingEls = $('.edit-profile-following')

followingEls.each(function(){
    $(this).on('mouseover', function(){
        $(this).css('color', 'red').css('background', 'rgb(255, 213, 213)').css('border-color', 'rgb(255, 213, 213)').text('Unfollow')
    })
    $(this).on('mouseout', function(){
        $(this).css('color', 'black').css('background', 'white').css('border-color', 'rgb(216, 216, 216)').text('Following')
    })
})
