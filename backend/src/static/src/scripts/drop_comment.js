document.addEventListener('DOMContentLoaded', () => {
    const showCommentBtns = document.querySelectorAll('.show_comment');
    const allCommentsContainers = document.querySelectorAll('.comments_container');

    showCommentBtns.forEach((btn, index) => {
        btn.addEventListener('click', (event) => {
            event.preventDefault();

            const commentsContainer = allCommentsContainers[index];
            commentsContainer.classList.toggle('active');

            if (commentsContainer.classList.contains('active')) {
                btn.textContent = 'Скрыть комментарии';
            } else {
                btn.textContent = 'Показать комментарии';
            }
        });
    });

    const userNameElements = document.querySelectorAll('.answer_comment');
    const myCommentElements = document.querySelectorAll('.my_comment');

    userNameElements.forEach((userName, index) => {
        userName.addEventListener('click', (event) => {
            event.preventDefault();

            const myComment = userName.closest('.lectures_comments').querySelector('.my_comment');
            const review = userName.closest('.comment');
            const commenterName = review.querySelector('.user_name').textContent.trim();

            myComment.value = `${commenterName}, `;
        });
    });
});
