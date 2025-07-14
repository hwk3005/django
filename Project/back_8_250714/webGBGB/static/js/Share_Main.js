document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('create-group-btn');
    if (btn) {
        btn.addEventListener('click', function(e) {
            if (typeof joinGroupCount !== "undefined" && joinGroupCount >= 8) {
                alert('최대 8개의 그룹만 참여할 수 있습니다.');
                e.preventDefault(); // 페이지 이동 막기
            }
        });
    }
});
