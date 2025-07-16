// join2.js

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

// ID 중복 확인 상태를 추적하는 변수 추가
let isIdChecked = false; // 기본값은 false (중복 확인 안 됨)
let isEmailVerified = false; // 이메일 인증 상태 추가

// Document Object Model이 완전히 로드된 후 실행
document.addEventListener("DOMContentLoaded", function() {
    const isKakaoSignup = document.querySelector("input[name='is_kakao_signup']") && document.querySelector("input[name='is_kakao_signup']").value === 'true';

    // 일반 회원가입일 때만 비밀번호 유효성 검사 이벤트 리스너를 추가
    if (!isKakaoSignup) {
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
    }

    // 해시태그 기능 (이 부분은 변경 없음)
    const input = document.querySelector("input[name='group_keyword_input']");
    const addBtn = document.querySelector(".add_tag_btn");
    const outputArea = document.querySelector(".group_keyword_output");
    const hiddenInput = document.querySelector("#group_keywords_hidden");
    const tagLinks = document.querySelectorAll(".tags a");
    const addedTags = new Set();

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
            link.classList.remove('selected');
          }
        });
      };

      tag.appendChild(delBtn);
      outputArea.appendChild(tag);
      updateHiddenInput();
    }

    // input에서 태그 추가
    addBtn.addEventListener("click", () => {
      const tagText = input.value.trim();
      if (tagText) {
        addTag(tagText);
        input.value = "";
      }
    });

    input.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        e.preventDefault(); // 기본 Enter 동작 (폼 제출) 방지
        const tagText = input.value.trim();
        if (tagText) {
          addTag(tagText);
          input.value = "";
        }
      }
    });

    // 태그 링크 클릭으로 태그 추가
    tagLinks.forEach(link => {
      link.addEventListener("click", (e) => {
        e.preventDefault();
        const tagText = e.target.textContent.trim().replace(/^#/, ''); // # 제거
        if (!addedTags.has(tagText)) {
          addTag(tagText);
          e.target.classList.add('selected'); // 선택된 태그 시각적 표시
        } else {
            // 이미 선택된 태그를 다시 클릭하면 삭제
            const tagElements = outputArea.querySelectorAll('.added-tag');
            tagElements.forEach(tagEl => {
                if (tagEl.textContent.replace('×', '').trim() === tagText) {
                    tagEl.querySelector('.tag-delete').click(); // 삭제 버튼 클릭 이벤트 트리거
                }
            });
          e.target.classList.remove('selected');
        }
      });
    });

    // ID 중복 확인 (일반 회원가입 시에만 필요)
    const checkIdButton = document.getElementById("checkIdButton");
    const idInput = document.querySelector("input[name='id']");
    // const idCheckMessage = document.querySelector(".id_check_message"); // 이 요소는 더 이상 사용하지 않음

    // CSRF 토큰을 가져오는 함수 (jQuery 사용하지 않으므로 직접 구현)
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

    if (checkIdButton && idInput && !isKakaoSignup) { // 일반 회원가입일 때만 활성화
        checkIdButton.addEventListener("click", function(e) {
            e.preventDefault(); // 기본 동작 방지 (폼 제출 등)
            const userId = idInput.value.trim();

            if (!userId) {
                alert("아이디를 입력해주세요.");
                isIdChecked = false;
                return;
            }

            // AJAX 요청
            fetch('/member/check-id/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: new URLSearchParams({
                    'user_id': userId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    alert("이미 사용중인 아이디입니다."); // alert으로 변경
                    isIdChecked = false;
                } else {
                    alert("사용 가능한 아이디입니다."); // alert으로 변경
                    isIdChecked = true;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('서버 오류가 발생했습니다.');
                isIdChecked = false;
            });
        });

        idInput.addEventListener("input", function() {
            // 아이디 입력 필드가 변경되면 중복 확인 상태를 초기화
            // alert 기반이므로, 시각적 피드백(테두리, 메시지) 제거
            isIdChecked = false;
        });
    }

    // 이메일 인증 기능 (일반 회원가입 시에만)
    const email1Input = document.querySelector("input[name='email1']");
    const email2Input = document.querySelector("input[name='email2']");
    const emailSelect = document.querySelector("select[name='email_select']");
    const sendVerificationCodeButton = document.getElementById("sendVerificationCode");
    const verificationCodeInput = document.getElementById("verificationCodeInput");
    const verifyCodeButton = document.getElementById("verifyCodeButton");
    const verificationCodeRow = document.getElementById("verificationCodeRow");
    const emailWarning = document.querySelector(".email_warning");
    const codeMessage = document.querySelector(".code_message");
    const timerDisplay = document.getElementById("timerDisplay");

    let timerInterval;
    let timeLeft = 0;

    // 카카오 회원가입 시 이메일 필드 초기값 설정 및 비활성화
    if (isKakaoSignup) {
        const kakaoEmail1Data = document.querySelector("input[name='email1_kakao_data']");
        const kakaoEmail2Data = document.querySelector("input[name='email2_kakao_data']");

        if (kakaoEmail1Data && kakaoEmail2Data) {
            email1Input.value = kakaoEmail1Data.value;
            email2Input.value = kakaoEmail2Data.value;
        }
        email1Input.readOnly = true;
        email2Input.readOnly = true;
        emailSelect.disabled = true; // 셀렉트 박스 비활성화

        // select 박스에서 해당 도메인 선택 (선택 사항)
        Array.from(emailSelect.options).forEach(option => {
            if (option.value === email2Input.value) { // 미리 채워진 email2Input.value와 일치하는 옵션 선택
                option.selected = true;
            }
        });
        // 카카오 회원가입 시에는 이메일 인증 버튼 비활성화
        if (sendVerificationCodeButton) {
            sendVerificationCodeButton.style.display = 'none';
        }
        if (verificationCodeRow) {
            verificationCodeRow.style.display = 'none';
        }
        isEmailVerified = true; // 카카오 가입은 이메일 인증된 것으로 간주
    } else {
        // 일반 회원가입 시 이메일 선택 기능
        emailSelect.addEventListener("change", function() {
            if (this.value === "") {
                email2Input.value = "";
                email2Input.readOnly = false;
            } else {
                email2Input.value = this.value;
                email2Input.readOnly = true;
            }
            // 이메일 변경 시 인증 상태 초기화
            isEmailVerified = false;
            emailWarning.style.display = 'none';
            codeMessage.style.display = 'none';
            if (verificationCodeRow) {
                verificationCodeRow.style.display = 'none';
            }
            if (sendVerificationCodeButton) {
                sendVerificationCodeButton.textContent = '인증번호 전송';
                sendVerificationCodeButton.disabled = false;
            }
            stopTimer();
        });

        // 이메일 입력 필드 변경 시 인증 상태 초기화
        [email1Input, email2Input].forEach(input => {
            input.addEventListener("input", function() {
                isEmailVerified = false;
                emailWarning.style.display = 'none';
                codeMessage.style.display = 'none';
                if (verificationCodeRow) {
                    verificationCodeRow.style.display = 'none';
                }
                if (sendVerificationCodeButton) {
                    sendVerificationCodeButton.textContent = '인증번호 전송';
                    sendVerificationCodeButton.disabled = false;
                }
                stopTimer();
            });
        });

        if (sendVerificationCodeButton) {
            sendVerificationCodeButton.addEventListener("click", function() {
                const email = `${email1Input.value.trim()}@${email2Input.value.trim()}`;
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

                if (!emailRegex.test(email)) {
                    alert("올바른 이메일 형식을 입력해주세요.");
                    email1Input.focus();
                    return;
                } else {
                    email1Input.style.border = "";
                    email2Input.style.border = "";
                }

                sendVerificationCodeButton.disabled = true;
                sendVerificationCodeButton.textContent = '전송중...';
                codeMessage.style.display = 'none';

                fetch('/member/send-join2-verification/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: new URLSearchParams({
                        'email1': email1Input.value.trim(),
                        'email2': email2Input.value.trim()
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(data.message);
                        if (verificationCodeRow) {
                            verificationCodeRow.style.display = 'table-row';
                        }
                        startTimer(300); // 5분 타이머 시작
                        sendVerificationCodeButton.textContent = '재전송';
                        sendVerificationCodeButton.disabled = false;
                    } else {
                        alert(data.message);
                        sendVerificationCodeButton.textContent = '인증번호 전송';
                        sendVerificationCodeButton.disabled = false;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('서버 오류가 발생했습니다.');
                    sendVerificationCodeButton.textContent = '인증번호 전송';
                    sendVerificationCodeButton.disabled = false;
                });
            });
        }

        if (verifyCodeButton) {
            verifyCodeButton.addEventListener("click", function() {
                const verificationCode = verificationCodeInput.value.trim();
                if (!verificationCode) {
                    codeMessage.textContent = "인증번호를 입력해주세요.";
                    codeMessage.style.color = "red";
                    codeMessage.style.display = 'block';
                    verificationCodeInput.style.border = "1.5px solid red";
                    return;
                } else {
                    codeMessage.style.display = 'none';
                    verificationCodeInput.style.border = "";
                }

                verifyCodeButton.disabled = true;
                verifyCodeButton.textContent = '인증 확인 중...';

                fetch('/member/verify-join2-code/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: new URLSearchParams({
                        'verification_code': verificationCode,
                        
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(data.message);
                        isEmailVerified = true;
                        codeMessage.textContent = "인증이 완료되었습니다.";
                        codeMessage.style.color = "green";
                        codeMessage.style.display = 'block';
                        verifyCodeButton.textContent = '인증 완료';
                        verifyCodeButton.disabled = true;
                        sendVerificationCodeButton.disabled = true; // 인증 완료 후 재전송 버튼 비활성화
                        stopTimer();
                    } else {
                        alert(data.message);
                        isEmailVerified = false;
                        codeMessage.textContent = data.message;
                        codeMessage.style.color = "red";
                        codeMessage.style.display = 'block';
                        verifyCodeButton.textContent = '인증하기';
                        verifyCodeButton.disabled = false;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('서버 오류가 발생했습니다.');
                    isEmailVerified = false;
                    verifyCodeButton.textContent = '인증하기';
                    verifyCodeButton.disabled = false;
                });
            });
        }
    }


    // 타이머 함수
    function startTimer(duration) {
        timeLeft = duration;
        stopTimer(); // 기존 타이머 중지
        timerInterval = setInterval(() => {
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

            if (timeLeft <= 0) {
                stopTimer();
                alert("인증번호 유효 시간이 만료되었습니다. 다시 요청해주세요.");
                if (sendVerificationCodeButton) {
                    sendVerificationCodeButton.textContent = '인증번호 재전송';
                    sendVerificationCodeButton.disabled = false;
                }
                if (verifyCodeButton) {
                    verifyCodeButton.disabled = false;
                    verifyCodeButton.textContent = '인증하기';
                }
                codeMessage.textContent = "인증번호가 만료되었습니다. 다시 전송해주세요.";
                codeMessage.style.color = "red";
                codeMessage.style.display = 'block';
                isEmailVerified = false;
            } else {
                timeLeft--;
            }
        }, 1000);
    }

    function stopTimer() {
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
            timerDisplay.textContent = "";
        }
    }


    // 폼 제출 시 유효성 검사
    const infoFrm = document.querySelector("form[name='infoFrm']");
    if (infoFrm) {
        infoFrm.addEventListener("submit", function(e) {
            // 카카오 회원가입이 아닌 경우에만 ID 중복 확인 및 이메일 인증 검사
            if (!isKakaoSignup) {
                // 아이디 중복 확인
                if (!isIdChecked) {
                    e.preventDefault();
                    alert("아이디 중복 확인을 해주세요.");
                    idInput.focus();
                    return;
                }
                // 이메일 인증 확인
                if (!isEmailVerified) {
                    e.preventDefault();
                    alert("이메일 인증을 완료해주세요.");
                    email1Input.focus();
                    return;
                }

                // 비밀번호 유효성 검사
                if (!validatePwLength()) {
                    e.preventDefault();
                    alert("비밀번호는 8자 이상이어야 합니다.");
                    pwInput.focus();
                    return;
                }

                // 비밀번호 일치 확인
                if (pwInput.value.trim() !== pw2Input.value.trim()) {
                    e.preventDefault();
                    alert("비밀번호와 비밀번호 확인이 일치하지 않습니다.");
                    pw2Input.focus();
                    return;
                }
            }
        });
    }

    // 취소 버튼 클릭 시 이전 페이지로 이동
    const cancelButton = document.getElementById("group_button_1");
    if (cancelButton) {
        cancelButton.addEventListener("click", function() {
            history.back();
        });
    }
});

const completeButton = document.getElementById("group_button_2");
if (completeButton && infoFrm) {
    completeButton.addEventListener("click", function () {
        infoFrm.requestSubmit();  // 폼을 정상 제출
    });
}