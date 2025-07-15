document.addEventListener('DOMContentLoaded', function() {
    // 그룹 만들기 버튼
    var createBtn = document.getElementById('create-group-btn');
    if (createBtn) {
        createBtn.addEventListener('click', function (e) {
            if (typeof joinGroupCount !== "undefined" && joinGroupCount >= 8) {
                alert('최대 8개의 그룹만 참여할 수 있습니다.');
                e.preventDefault();  // 페이지 이동 막기
            }
        });
    }
    // 그룹 참여하기 버튼
    var joinBtn = document.querySelector('.join-btn');
    if (joinBtn) {
        joinBtn.addEventListener('click', function (e) {
            if (typeof joinGroupCount !== "undefined" && joinGroupCount >= 8) {
                alert('최대 8개의 그룹만 참여할 수 있습니다.');
                e.preventDefault();
            }
        });
    }
});

// 로그아웃 상태일 때 그룹 참여 제한
function alertAndRedirectLogin() {
    alert("로그인 후 이용 가능합니다.");
    // window.location.href = "/member/login/";  // ← 로그인 페이지 URL로 수정하세요
    window.location.href = "/member/login/?next=" +
    encodeURIComponent(window.location.pathname);
};
