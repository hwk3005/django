$('#member_delete').on('click', function () {
  if (!confirm('정말 계정을 삭제하시겠습니까?')) return;

  $.ajax({
    url: '/mypage/member_delete/',
    type: 'POST',
    success: function (res) {
      alert(res.message);
      if (res.result === 'success') {
        window.location.href = '/';
      }
    },
    error: function () {
      alert('서버 오류가 발생했습니다.');
    }
  });
});
