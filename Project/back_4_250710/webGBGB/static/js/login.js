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

  // 로그인 페이지 로드 시 실행
  window.onload = function () {
    const savedId = getCookie('savedUserId');
    const userIdInput = document.getElementById('userId');
    const saveIdCheckbox = document.getElementById('saveID');

    if (savedId) {
      userIdInput.value = savedId;
      saveIdCheckbox.checked = true;
    }

    // 로그인 버튼 클릭 시 쿠키 저장 또는 삭제
    document.getElementById('loginBtn').addEventListener('click', function (e) {
      const userId = userIdInput.value;

      if (saveIdCheckbox.checked) {
        setCookie('savedUserId', userId, 7); // 7일 동안 저장
      } else {
        setCookie('savedUserId', '', -1); // 삭제
      }
    });
  };