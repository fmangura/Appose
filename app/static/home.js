
// $('.commentButton').on("click", function(){
//     const id = $(this).data('id');
//     commList = getComments(id);
//     if (commList.length > 0) {
//         for (let comment of commList){
//             $(this).parent().parent().append(`<p>${comment.text}${comment.user.username}</p>`)
//         }
//     };
//     $(this).parent().parent().append('<br><p class="card-subtitle text-muted font-sm">...more comments</p>');

// })
    
// async function getComments(id) {
//     console.log(`/posts/comments/${id}`)
//     let data = await axios.get(`/posts/comments/${id}`)
//     let commList = data.data.comments
//     return commList
// }

$(document).on("click", '.post-content', function(){
    let id = $(this).data('id');
    return viewPost(id);
})

// $('.commentButton').on("hover", function(){
//     let id = $(this).data('id');
//     $('#commentFor-'+id).toggleClass('hidden');
// })

$('.commentButton').on("click", function(){
    let id = $(this).data('id');
    $('#commentFor-'+id).toggleClass('hidden');
    $('#comment-'+id).toggleClass('fa-solid fa-regular');

    if (!$('#statisticsFor-'+id).hasClass('hidden')){
        $('#statisticsFor-'+id).toggleClass('hidden');
    }
})

$('.statButton').on("click", function(){
    let id = $(this).data('id');
    $('#statisticsFor-'+id).toggleClass('hidden');

    if (!$('#commentFor-'+id).hasClass('hidden')){
        $('#commentFor-'+id).toggleClass('hidden');
    }
})

$('.likeButton').on('click', function(){
    let id = $(this).data('id');
    let button = $('#like-'+id)
    if (button.hasClass('fa-regular')){
        button.toggleClass('fa-solid fa-regular');
        doLike(id);

    }else{
        button.toggleClass('fa-solid fa-regular');
        unLike(id);
    }

})

$(document).on('click', '.fa-paperclip', function(){
    $('#attachInput').toggleClass('hidden');
})

$(document).on('change', '.form-range', function(){
    let id = $(this).data('id');
    let input = $(this).val();
    agreeValue(id, input)
    $(this).attr('disabled', true)
})

$(document).on('click', '.expand-right-post', function(){
    let id = $(this).data('id');
    $('#left-post-'+id).toggleClass('col-1');
    $('#left-post-'+id).toggleClass('hidden');
    $('.expand-right-post').toggleClass('fa-caret-left fa-xmark');
    $('#right-stat-bar'+id).toggleClass('hidden');
    if ($('#right-post-'+id).hasClass('col-1')) {
        $('#right-post-'+id).toggleClass('col-1');
        $('#right-post-'+id).toggleClass('hidden');
        $('#left-stat-bar'+id).toggleClass('hidden');
    }
})

$(document).on('click', '.expand-left-post', function(){
    let id = $(this).data('id');
    $('#right-post-'+id).toggleClass('col-1');
    $('#right-post-'+id).toggleClass('hidden');
    $('.expand-left-post').toggleClass('fa-caret-right fa-xmark');
    $('#left-stat-bar'+id).toggleClass('hidden');
        if ($('#left-post-'+id).hasClass('col-1')) {
            $('#left-post-'+id).toggleClass('col-1');
            $('#left-post-'+id).toggleClass('hidden');
            $('#right-stat-bar'+id).toggleClass('hidden');
        }
})

$(document).on('click', '.go-top', function(){
    window.scrollTo(0,0);
})

$('.agreement-input').dblclick(function(){
    let id = $(this).data('id');
    $('#form-range-'+ id).prop('disabled', false)
})


async function agreeValue(id, input) {
    const res = await axios.post(`/agreement`, {
        post_id:`${id}`,
        input_value:`${input}`
    })

}

async function viewPost(id) {
    return await axios.get(`/posts/comments/${id}`);
}

async function doLike(id) {
    await axios.post(`/posts/like/${id}`);
}

async function unLike(id) {
    await axios.delete(`/posts/like/${id}/delete`);
}




