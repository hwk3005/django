// 쿠키 설정 함수
function setCookie(name, value, days) {
  const expires = new Date();
  expires.setDate(expires.getDate() + days);
  document.cookie = name + '=' + encodeURIComponent(value) + '; path=/; expires=' + expires.toUTCString();
}

// 쿠키 가져오기 함수
function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [key, val] = cookie.trim().split('=');
    if (key === name) return decodeURIComponent(val);
  }
  return '';
}

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', function() {
  const savedId = getCookie('savedUserId');
  const userIdInput = document.getElementById('id');
  const saveIdCheckbox = document.getElementById('saveID');
  const loginForm = document.querySelector('form[name="loginFrm"]');

  // 저장된 아이디가 있으면 입력창에 설정하고 체크박스 체크
  if (savedId) {
    userIdInput.value = savedId;
    saveIdCheckbox.checked = true;
  }

  // 폼 제출 시 쿠키 처리
  loginForm.addEventListener('submit', function(e) {
    const userId = userIdInput.value.trim();

    if (saveIdCheckbox.checked && userId) {
      // 체크박스가 체크되어 있고 아이디가 입력되어 있으면 쿠키에 저장
      setCookie('savedUserId', userId, 7); // 7일 동안 저장
    } else {
      // 체크박스가 체크되지 않았으면 쿠키 삭제
      setCookie('savedUserId', '', -1);
    }
  });

  // 체크박스 상태 변경 시 즉시 쿠키 처리
  saveIdCheckbox.addEventListener('change', function() {
    const userId = userIdInput.value.trim();
    
    if (!this.checked) {
      // 체크박스가 해제되면 쿠키 삭제
      setCookie('savedUserId', '', -1);
    } else if (userId) {
      // 체크박스가 체크되고 아이디가 있으면 쿠키 저장
      setCookie('savedUserId', userId, 7);
    }
  });
});
