const showCommentBtn = document.getElementById('show_comment'),
      allComments = document.getElementById('comments_container'),
      userName = document.getElementById('user_name'),
      myComment = document.getElementById('my_comment');

      
showCommentBtn.addEventListener('click', (event) => {
    event.preventDefault();

    allComments.classList.toggle('active');

    if(allComments && allComments.classList.contains('active')){
        showCommentBtn.textContent = 'Скрыть комментарии';
    } else{
        showCommentBtn.textContent = 'Показать комментарии';
    }   
})

userName.addEventListener('click', (event) => {
    event.preventDefault();

    myComment.value = userName.textContent + ',';
})

