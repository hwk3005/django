// join2.js

// 해시태그 기능
const input = document.querySelector("input[name='group_keyword_input']");
const addBtn = document.querySelector(".add_tag_btn");
const outputArea = document.querySelector(".group_keyword_output");
const hiddenInput = document.querySelector("#group_keywords_hidden");
const tagLinks = document.querySelectorAll(".tags a");
const addedTags = new Set();

// ID 중복 확인 상태를 추적하는 변수 추가
let isIdChecked = false; // 기본값은 false (중복 확인 안 됨)

// hidden input에 저장
function updateHiddenInput() {
  hiddenInput.value = Array.from(addedTags).join(",");
}

// 태그 추가 함수 (중복만 방지)
function addTag(tagText) {
  if (!tagText || addedTags.has(tagText)) return;

  addedTags.add(tagText);

  const tag = document.createElement("div");
  tag.className = "added-tag";
  tag.textContent = tagText;

  const delBtn = document.createElement("span");
  delBtn.className = "tag-delete";
  delBtn.innerHTML = "&times;";

  delBtn.onclick = () => {
    addedTags.delete(tagText);
    tag.remove();
    updateHiddenInput();

    tagLinks.forEach(link => {
      if (link.textContent.trim() === tagText) {
        link.classList.remove("clicked");
      }
    });
  };

  tag.appendChild(delBtn);
  outputArea.appendChild(tag);
  updateHiddenInput();
}

// 인풋 기반 추가 (언어 제한 없음)
function addTagFromInput() {
  const value = input.value.trim();
  const tagText = `#${value}`;
  if (!value) return;
  addTag(tagText);
  input.value = "";
}

// Enter 키로 입력
input.addEventListener("keydown", function(e) {
  if (e.key === "Enter") {
    e.preventDefault();
    addTagFromInput();
  }
});

// + 버튼 클릭
addBtn.addEventListener("click", addTagFromInput);

// 아래 해시태그 클릭 시 추가
tagLinks.forEach(link => {
  link.addEventListener("click", function(e) {
    e.preventDefault();
    const tagText = this.textContent.trim();
    addTag(tagText);
    this.classList.add("clicked");
  });
});


// 비밀번호 유효성 검사 및 일치 확인
const pwInput = document.querySelector("input[name='pw']");
const pw2Input = document.querySelector("input[name='pw2']");

const pwWarning = document.createElement("div");
pwWarning.style.color = "red";
pwWarning.style.fontSize = "15px";
pwWarning.style.marginTop = "20px";
pwWarning.style.marginLeft = "15px";
pwWarning.textContent = "8자 이상 입력하셔야 합니다.";

const matchMessage = document.createElement("div");
matchMessage.style.fontSize = "15px";
matchMessage.style.marginTop = "20px";
matchMessage.style.marginLeft = "15px";

function validatePwLength() {
  const pw = pwInput.value.trim();
  if (pw.length < 8) {
    pwInput.style.border = "1.5px solid red";
    if (!pwInput.parentNode.contains(pwWarning)) {
      pwInput.parentNode.appendChild(pwWarning);
    }
    return false;
  } else {
    pwInput.style.border = "";
    if (pwInput.parentNode.contains(pwWarning)) {
      pwInput.parentNode.removeChild(pwWarning);
    }
    return true;
  }
}

pwInput.addEventListener("blur", validatePwLength);

pw2Input.addEventListener("keyup", function () {
  const pw = pwInput.value.trim();
  const pw2 = pw2Input.value.trim();

  if (pw.length < 8) {
    pw2Input.style.border = "";
    if (pw2Input.parentNode.contains(matchMessage)) {
      pw2Input.parentNode.removeChild(matchMessage);
    }
    return;
  }

  if (pw2 === "") {
    pw2Input.style.border = "";
    if (pw2Input.parentNode.contains(matchMessage)) {
      pw2Input.parentNode.removeChild(matchMessage);
    }
  } else if (pw === pw2) {
    pw2Input.style.border = "1.5px solid green";
    matchMessage.textContent = "비밀번호가 일치합니다.";
    matchMessage.style.color = "green";
    if (!pw2Input.parentNode.contains(matchMessage)) {
      pw2Input.parentNode.appendChild(matchMessage);
    }
  } else {
    pw2Input.style.border = "1.5px solid red";
    matchMessage.textContent = "비밀번호가 일치하지 않습니다.";
    matchMessage.style.color = "red";
    if (!pw2Input.parentNode.contains(matchMessage)) {
      pw2Input.parentNode.appendChild(matchMessage);
    }
  }
});


// ID 중복 체크 (jQuery 사용)
$(document).ready(function() {
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  $('#checkIdBtn').click(function(e) {
    e.preventDefault();

    const userId = $('input[name="id"]').val().trim();
    if (userId === "") {
      alert("아이디를 입력해주세요.");
      // 아이디 입력값이 없으면 중복 확인 상태를 false로 유지
      isIdChecked = false;
      return;
    }

    const csrftoken = getCookie('csrftoken');

    $.ajax({
      url: '/member/check-id/',
      method: 'POST',
      data: {
        id: userId,
        csrfmiddlewaretoken: csrftoken
      },
      dataType: 'json',
      success: function(response) {
        if (response.available) {
          alert("사용 가능한 아이디입니다.");
          $('input[name="id"]').css('border', '2px solid green');
          isIdChecked = true; // 사용 가능한 아이디이면 중복 확인 완료
        } else {
          alert("중복된 아이디입니다.");
          $('input[name="id"]').css('border', '2px solid red');
          isIdChecked = false; // 중복된 아이디이면 중복 확인 실패
        }
      },
      error: function(xhr, status, error) {
        console.log("AJAX Error:", xhr.responseText);
        console.log("Status:", status);
        console.log("Error:", error);
        alert("서버와 통신 중 오류가 발생했습니다. 나중에 다시 시도해주세요.");
        isIdChecked = false; // 오류 발생 시 중복 확인 실패
      }
    });
  });

  // ID 입력란 변경 감지 (중복 확인 상태 초기화)
  $('input[name="id"]').on('input', function() {
    if (isIdChecked) { // 이전에 중복 확인을 완료한 상태였다면
      
      isIdChecked = false; // 중복 확인 상태 초기화
      $('input[name="id"]').css('border', ''); // 테두리 색상 초기화
    }
  });
});

// 취소 버튼 클릭 시 홈으로
document.querySelector("#group_button_1").addEventListener("click", function () {
  if (confirm("회원가입을 취소하시겠습니까? 입력한 정보가 모두 사라집니다.")) {
    window.location.href = '/';
  }
});

// 필수 항목 기입 및 폼 제출
document.querySelector("#group_button_2").addEventListener("click", function () {
  const name = document.querySelector("input[name='name']").value.trim();
  const id = document.querySelector("input[name='id']").value.trim();
  const pw = document.querySelector("input[name='pw']").value.trim();
  const pw2 = document.querySelector("input[name='pw2']").value.trim();
  const email1 = document.querySelector("input[name='email1']").value.trim();
  const email2 = document.querySelector("input[name='email2']").value.trim();

  // ID 중복 확인 여부 검사 추가
  if (!isIdChecked) {
    alert("아이디 중복 확인을 완료해주세요.");
    return;
  }

  if (!name || !id || !pw || !pw2 || !email1 || !email2) {
    alert("모든 필수 항목을 입력해주세요.");
    return;
  }

  if (pw.length < 8) {
    alert("비밀번호는 8자 이상이어야 합니다.");
    return;
  }

  if (pw !== pw2) {
    alert("비밀번호가 일치하지 않습니다.");
    return;
  }

  // 폼 제출 전에 method를 POST로 변경
  document.infoFrm.method = "post";
  document.infoFrm.action = "/member/join3/";
  document.infoFrm.submit();
});


// Email 선택 시 자동 입력 및 수정 불가
document.addEventListener("DOMContentLoaded", function () {
  const emailSelect = document.querySelector(".email-select");
  const email2Input = document.querySelector(".email2");

  emailSelect.addEventListener("change", function () {
    const selected = this.value;

    if (selected === "직접입력") {
      email2Input.value = "";
      email2Input.readOnly = false;
      email2Input.focus();
    } else {
      email2Input.value = selected;
      email2Input.readOnly = true;
    }
  });
});