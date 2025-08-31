document.addEventListener('DOMContentLoaded', () => {

  /* 펼치기 */
  document.querySelectorAll('.comment_item').forEach(item => {
    const moreBtn = item.querySelector('.btn_more_body');
    if (!moreBtn) return;

    if (item.classList.contains('overflow')) {
      moreBtn.style.display = 'block';
    } else {
      moreBtn.style.display = 'none';
    }

    moreBtn.addEventListener('click', () => {
      const isActive = item.classList.toggle('active');
      moreBtn.classList.toggle('active', isActive);
      moreBtn.querySelector('.text').textContent = isActive ? '접기' : '펼치기';

      const icon = moreBtn.querySelector('i');
      if (icon) {
        icon.classList.toggle('fa-circle-arrow-up', isActive);
        icon.classList.toggle('fa-circle-arrow-down', !isActive);
      }

      const thumb = item.querySelector('.comment_thumb_box');
      const swiper = item.querySelector('.comment_swiper_wrap');
      if (thumb && swiper) {
        thumb.style.display = isActive ? 'none' : 'block';
        swiper.style.display = isActive ? 'block' : 'none';
      }
    });
  });




  /* 이미지 썸네일 클릭 시 Swiper 보기 */
  document.querySelectorAll('.comment_thumb_box').forEach(box => {
    box.addEventListener('click', () => {
      const item = box.closest('.comment_item');
      if (item) {
        item.classList.add('overflow', 'active');
        const thumb = item.querySelector('.comment_thumb_box');
        const swiper = item.querySelector('.comment_swiper_wrap');
        if (thumb) thumb.style.display = 'none';
        if (swiper) swiper.style.display = 'block';
      }
    });
  });
   


// 리뷰박스 삭제 요청 및 삭제 스크립트
$(document).on('click', '.deleteBtn', function () {
  const $commentItem = $(this).closest('.comment_item');
  const reviewId = $commentItem.data('id'); // HTML에서 data-id로 지정된 값
  const cToken = $('meta[name="csrf-token"]').attr('content');

  if (!confirm('정말 삭제하시겠습니까?')) return;

  $.ajax({
    url: '/mypage/review_delete/',  // 백엔드 URL에 맞게 수정
    type: 'post',
    headers: { 'X-CSRFToken': cToken },
    data: { 'review_id': reviewId },
    success: function (data) {
      if (data.result === 'success') {
        $commentItem.remove(); // DOM에서 제거

        // 리뷰 개수 갱신
        const $countSpan = $("#my_review_count");
        const currentCount = parseInt($countSpan.text().replace(/[^\d]/g, ''), 10); // 괄호 제외 숫자 추출
        const newCount = currentCount - 1;

        if (newCount <= 0) {
          $countSpan.text('(0)');
        } else {
          $countSpan.text(`(${newCount})`);
        }
      } else {
        alert('삭제 실패: ' + data.message);
      }
    },
    error: function () {
      alert('서버 오류');
    }
  });
});

});//맨위랑 연결



//리뷰박스 클릭시 상세페이지 이동


document.addEventListener('DOMContentLoaded', function () {
  console.log("✅ DOMContentLoaded 실행됨");

  document.addEventListener('click', function (e) {
    console.log("✅ document 클릭 감지됨");

    // 삭제 버튼이면 상세페이지 이동 막기
    if (e.target.closest('.deleteBtn')) {
      console.log("삭제 버튼 클릭 - 이동 막음");
      return;
    }
    if (e.target.closest('.btn_more_body')) {
      console.log("펼치기 버튼 클릭 - 이동 막음");
      return;
    }
    if (e.target.closest('.comment_img_box')) {
      console.log("리뷰이미지 클릭 - 이동 막음");
      return;
    }
    if (e.target.closest('.btn_like')) {
      console.log("좋아요 클릭 - 이동 막음");
      return;
    }
    if (e.target.closest('.btn_reply')) {
      console.log("댓글 클릭 - 이동 막음");
      return;
    }
    if (e.target.closest('.comment_thumb_box')) {
      console.log("이미지 클릭 - 이동 막음");
      return;
    }

    const commentItem = e.target.closest('.comment_item');
    console.log("👉 commentItem:", commentItem);

    if (!commentItem) return;

    const bookId = commentItem.dataset.bookId;
    console.log("📘 클릭된 bookId:", bookId);

    window.location.href = `/booksearch/detail/${bookId}/`;
  });
});
