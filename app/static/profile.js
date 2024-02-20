$( document ).on('click', '.fa-trash-can', function(){
    let id = $(this).data('id')
    deletePost(id)
})

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

async function deletePost(id) {
    await axios.delete(`/posts/${id}/delete`)
    location.reload()
}
