// 내그룹박스 나가기 요청 및 나가기 스크립트
$(document).on('click', '.outBtn', function () {
  const $bookBox = $(this).closest('.bookbox');
  const id = $bookBox.data('id'); // HTML에서 data-id로 지정된 값
  const cToken = $('meta[name="csrf-token"]').attr('content');

  if (!confirm('정말 그룹에서 나가시겠습니까?')) return;

  $.ajax({
    url: '/mypage/mygroup_delete/',  // 백엔드 URL에 맞게 수정
    type: 'post',
    headers: { 'X-CSRFToken': cToken },
    data: { 'id': id },
    success: function (data) {
      if (data.result === 'success') {
        
        $bookBox.remove(); // DOM에서 제거
        
        // 나갔을때 개수 갱신
        const $countSpan = $("#my_group_count");
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
        alert("그룹에서 나왔습니다.")
      },
      error: function () {
        alert('서버 오류');
      }
    });
  });


