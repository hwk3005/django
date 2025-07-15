function toggleBookmark(button) {
    const bookId = button.getAttribute('data-book-id');
    let cToken = $('meta[name="csrf-token"]').attr('content');
    const icon = button.querySelector('i');
    if (!icon) {
        console.warn('아이콘 없음');
        return;
    }

    $.ajax({
        url: '/bookmark/create/',
        type: 'post',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': cToken },
        data: JSON.stringify({ book_id: bookId }),
        success: function(data) {
            if (data.bookmarked !== undefined) {
                icon.classList.remove('fa-solid', 'fa-regular');
                icon.classList.add(data.bookmarked ? 'fa-solid' : 'fa-regular');
                button.classList.toggle('active', data.bookmarked);
            }
        },
        error: function() {
        }
    });

    // 애니메이션 효과는 성공 후에 처리하는 게 더 자연스러울 수 있습니다.
    icon.classList.add('fading-out');
    setTimeout(() => {
        icon.classList.remove('fading-out');
    }, 100);
}