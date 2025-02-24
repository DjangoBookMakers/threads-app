document.addEventListener('DOMContentLoaded', function() {
    // 좋아요 버튼 동작처리
    const likeButtons = document.querySelectorAll('.like-button');
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const currentLikes = parseInt(this.dataset.likes);
            this.dataset.likes = currentLikes + 1;
            this.querySelector('.likes-count').textContent = currentLikes + 1;
        });
    });

    // 시간 표시 형식 변환
    const timestamps = document.querySelectorAll('.timestamp');
    timestamps.forEach(timestamp => {
        const date = new Date(timestamp.dataset.time);
        timestamp.textContent = date.toLocaleString();
    });
});