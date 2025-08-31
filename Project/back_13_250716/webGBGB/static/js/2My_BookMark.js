// 북마크박스 삭제 요청 및 삭제 스크립트
$(document).on('click', '.bookmarkBtn', function () {
  const $bookBox = $(this).closest('.bookbox');
  const bookmarkId = $bookBox.data('id'); // HTML에서 data-id로 지정된 값
  const cToken = $('meta[name="csrf-token"]').attr('content');

  if (!confirm('정말 북마크를 삭제하시겠습니까?')) return;

  $.ajax({
    url: '/mypage/bookmark_delete/',  // 백엔드 URL에 맞게 수정
    type: 'post',
    headers: { 'X-CSRFToken': cToken },
    data: { 'bookmark_id': bookmarkId },
    success: function (data) {
      if (data.result === 'success') {
        $bookBox.remove(); // DOM에서 제거

        // 리뷰 개수 갱신
        const $countSpan = $("#my_bookmark_count");
        if ($countSpan.length > 0) {
          const text = $countSpan.text();  // text 정의 없으면 에러남
          console.log("기존 텍스트:", text); // 예: "(3)"

          const currentCount = parseInt(text.replace(/[^\d]/g, ''), 10);
          const newCount = currentCount - 1;
          if (newCount <= 0) {
            $countSpan.text('(0)');
          } else {
            $countSpan.text(`(${newCount})`);
          }
        } else {
          alert('삭제 실패: ' + data.message);
        }
        
        };
      },
      error: function () {
        alert('서버 오류');
      }
    });
  });




//리뷰박스 클릭시 상세페이지 이동


document.addEventListener('DOMContentLoaded', function () {
  console.log("✅ DOMContentLoaded 실행됨");

  document.addEventListener('click', function (e) {
    console.log("✅ document 클릭 감지됨");

    // ❗ 삭제 버튼이면 상세페이지 이동 막기
    if (e.target.closest('.bookmarkBtn')) {
      console.log("북마크제거버튼 클릭 - 이동 막음");
      return;
    }

    const bookBox = e.target.closest('.bookbox');
    console.log("bookBox:", bookBox);

    if (!bookBox) return;

    const bookId = bookBox.dataset.bookId;
    console.log("📘 클릭된 bookId:", bookId);

    window.location.href = `/booksearch/detail/${bookId}/`;
  });
});


