

// 관심 분야 (해시태그) 기능 추가 시작
const input = document.querySelector("input[name='group_keyword_input']");
const addBtn = document.querySelector(".add_tag_btn");
const outputArea = document.querySelector(".group_keyword_output");
const hiddenInput = document.querySelector("#group_keywords_hidden");
const tagLinks = document.querySelectorAll(".tags a");
const addedTags = new Set(); // Set을 사용하여 중복 태그 방지

// hidden input에 현재 태그들을 저장하는 함수
function updateHiddenInput() {
  hiddenInput.value = Array.from(addedTags).join(",");
}

// 태그를 추가하는 함수 (중복 방지 로직 포함)
function addTag(tagText) {
  // 태그 텍스트가 없거나 이미 추가된 태그이면 아무것도 하지 않음
  if (!tagText || addedTags.has(tagText)) return;

  addedTags.add(tagText); // Set에 태그 추가

  const tag = document.createElement("div");
  tag.className = "added-tag";
  tag.textContent = tagText;

  const delBtn = document.createElement("span");
  delBtn.className = "tag-delete";
  delBtn.innerHTML = "&times;"; // 닫기 버튼 (X)

  // 닫기 버튼 클릭 시 태그 삭제
  delBtn.onclick = () => {
    addedTags.delete(tagText); // Set에서 태그 삭제
    tag.remove(); // DOM에서 태그 요소 삭제
    updateHiddenInput(); // hidden input 업데이트

    // 미리 정의된 태그 목록에서 클릭된 상태 제거
    tagLinks.forEach(link => {
      if (link.textContent.trim() === tagText) {
        link.classList.remove("clicked");
      }
    });
  };

  tag.appendChild(delBtn); // 태그 요소에 닫기 버튼 추가
  outputArea.appendChild(tag); // 출력 영역에 태그 추가
  updateHiddenInput(); // hidden input 업데이트
}

// 입력 필드 기반으로 태그 추가 (Enter 키 또는 + 버튼)
function addTagFromInput() {
  const value = input.value.trim();
  const tagText = `#${value}`; // 항상 #을 붙이도록 수정 (필요에 따라 조정)
  if (!value) return; // 입력값이 없으면 추가하지 않음
  addTag(tagText);
  input.value = ""; // 입력 필드 초기화
}

// Enter 키로 태그 추가
input.addEventListener("keydown", function(e) {
  if (e.key === "Enter") {
    e.preventDefault(); // 기본 Enter 동작(폼 제출) 방지
    addTagFromInput();
  }
});

// + 버튼 클릭으로 태그 추가
addBtn.addEventListener("click", addTagFromInput);

// 미리 정의된 해시태그 클릭 시 추가
tagLinks.forEach(link => {
  link.addEventListener("click", function(e) {
    e.preventDefault(); // 기본 링크 동작 방지
    const tagText = this.textContent.trim();
    addTag(tagText);
    this.classList.add("clicked"); // 클릭된 태그에 시각적 표시 (CSS 필요)
  });
});

// 페이지 로드 시 기존 관심 분야 로드 (DOMContentLoaded 밖으로 이동)
document.addEventListener("DOMContentLoaded", function() {
  // 기존 이메일 선택 로직은 여기에 유지
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

  // member_update.html에서 hidden input에 설정된 기존 genres 값을 가져옴
  const initialGenres = hiddenInput.value;
  if (initialGenres) {
    // 콤마로 분리된 문자열을 배열로 만들고 각 태그를 추가
    initialGenres.split(',').forEach(genre => {
      // # 접두사가 이미 있다면 제거하지 않고, 없다면 추가하여 일관성 유지 (views.py와 연동하여 조정)
      const formattedGenre = genre.startsWith('#') ? genre.trim() : `#${genre.trim()}`;
      addTag(formattedGenre);

      // 미리 정의된 태그 목록에서 현재 태그와 일치하는 것이 있다면 'clicked' 클래스 추가
      tagLinks.forEach(link => {
        if (link.textContent.trim() === formattedGenre) {
          link.classList.add("clicked");
        }
      });
    });
  }
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
  if (pw.length > 0 && pw.length < 8) { // 비밀번호가 입력되었을 때만 길이 검사
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

  // 비밀번호 입력이 없으면 메시지 숨김
  if (pw === "" && pw2 === "") {
    pwInput.style.border = "";
    pw2Input.style.border = "";
    if (pwInput.parentNode.contains(pwWarning)) {
        pwInput.parentNode.removeChild(pwWarning);
    }
    if (pw2Input.parentNode.contains(matchMessage)) {
      pw2Input.parentNode.removeChild(matchMessage);
    }
    return;
  }

  // 첫 번째 비밀번호가 8자 미만일 때는 메시지 표시
  if (pw.length > 0 && pw.length < 8) {
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


// 취소 버튼 클릭 시 뒤로가기
document.querySelector("#group_button_1").addEventListener("click", function () {
  if (confirm("회원정보 수정을 취소하시겠습니까? 입력한 정보가 모두 사라집니다.")) {
    window.history.back();
  }
});

// 완료 버튼 클릭 시 유효성 검사 및 폼 제출
document.querySelector("#group_button_2").addEventListener("click", function () {
  const name = document.querySelector("input[name='name']").value.trim();
  const email1 = document.querySelector("input[name='email1']").value.trim();
  const email2 = document.querySelector("input[name='email2']").value.trim();
  const pw = document.querySelector("input[name='pw']").value.trim();
  const pw2 = document.querySelector("input[name='pw2']").value.trim();

  // 필수 항목 검사
  if (!name || !email1 || !email2) {
    alert("이름과 이메일은 필수 항목입니다.");
    return;
  }

  // 비밀번호 검증 (입력된 경우만)
  if (pw.length > 0) { // 비밀번호가 입력되었을 때만 검사
    if (pw.length < 8) {
      alert("비밀번호는 8자 이상이어야 합니다.");
      return;
    }

    if (pw !== pw2) {
      alert("비밀번호가 일치하지 않습니다.");
      return;
    }
  } else if (pw2.length > 0) { // pw가 비어있는데 pw2에만 값이 있는 경우
      alert("비밀번호를 입력해주세요.");
      return;
  }

  // 폼 제출
  document.updateFrm.submit();
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