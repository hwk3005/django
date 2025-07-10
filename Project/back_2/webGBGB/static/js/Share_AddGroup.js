// 책 검색 (모달창)
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("book_search_modal"); 
    const overlay = modal.querySelector(".modal_overlay");
    const closeBtn = modal.querySelector(".modal_close");
    const input = document.getElementById("book_search_input_modal");
    const searchBtn = document.getElementById("modal_search_btn");
    const results = document.querySelector(".modal_results");
    const selectedDisplay = document.getElementById("selected-book-display");
    // 🔹 form의 hidden input 요소들
    const inputTitle = document.getElementById("input_book_title");
    const inputAuthor = document.getElementById("input_book_author");
    const inputCover = document.getElementById("input_book_cover");
    const inputISBN = document.getElementById("input_book_isbn");
    // 🔸 모달 열기
    function openModal() {
    modal.style.display = "block";
    input.focus();
    }
    // 🔸 모달 닫기
    function closeModal() {
    modal.style.display = "none";
    results.innerHTML = "";
    input.value = "";
    }
    // 🔹 모달 열기 트리거
    document.addEventListener("click", function (e) {
    if (e.target.closest("#book_search_trigger")) {
        e.preventDefault();
        openModal();
    }
    });
    // 🔹 모달 닫기
    overlay.addEventListener("click", closeModal);
    closeBtn.addEventListener("click", closeModal);
    closeBtn.addEventListener("click", function (e) {
    e.preventDefault();
    closeModal();
    });
    
    // 책 검색, 카카오 API
    searchBtn.addEventListener("click", function () {
        const query = searchInput.value.trim();
        if (!query) {
        resultsContainer.innerHTML = "<p>검색어를 입력해주세요.</p>";
        return;
        }
        fetch(`/shareMain/ajax_search?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            const books = data.books || [];
            if (books.length === 0) {
            resultsContainer.innerHTML = "<p>검색 결과가 없습니다.</p>";
            return;
            }
            resultsContainer.innerHTML = books.map(book => `
            <div class="modal_result" data-title=" ${book.title}">
                <div class="modal_book_item">
                    <img src="${book.cover}" alt="${book.title}" />
                </div>
                <div class="modal_book_info">
                    <h3>${book.title}</h3>
                    <p><strong>저자:</strong> ${book.author}</p>
                    <p><strong>출판사:</strong> ${book.publisher}</p>
                    <p class="modal_description"> ${ book.description }</p>
                </div>
                <div class="modal_book_select">
                    <button type="button" class="modal_book_select_btn"
                        data-title="${book.title}"
                        data-author="${book.author}"
                        data-cover="${book.cover}"
                        data-isbn="${book.isbn}"
                    >선택</button>
                </div>
            </div>
            `).join("");
        })
        .catch(error => {
            console.error("책 검색 오류:", error);
            resultsContainer.innerHTML = "<p>검색 중 오류가 발생했습니다.</p>";
        });
    });
    
    // 📌 책 선택 시 - form에 데이터 삽입 + UI 업데이트
    results.addEventListener("click", function (e) {
    if (e.target.classList.contains("modal_book_select_btn")) {
        const bookItem = e.target.closest(".modal_book_item");
        const img = bookItem.querySelector("img").getAttribute("src");
        const title = bookItem.querySelector("h3").innerText;
        const author = bookItem.querySelector(".modal_author").innerText.replace("저자:", "").trim();
        const isbn = bookItem.getAttribute("data-isbn");
        // ✅ hidden input에 값 세팅
        inputTitle.value = title;
        inputAuthor.value = author;
        inputCover.value = img;
        inputISBN.value = isbn;
        // ✅ 선택된 책 표시 (화면)
        selectedDisplay.innerHTML = `
        <div class="selected_book_display">
            <a href="#" id="book_search_trigger">
            <div class="selected_book_img">
                <div class="tooltip_wrapper">
                <img src="${img}" alt="">
                <div class="custom_tooltip">변경<br></div>
                </div>
            </div>
            </a>
            <div class="selected_book_text">
            <span>${title}</span>
            <p>${author}</p>
            </div>
        </div>
        `;
        closeModal();
    }
    });
});


/* 해시태그 기능 추가
    1) input에서 Enter로 태그 추가
    2) + 버튼 클릭으로 태그 추가
    3) 한글만 입력 가능
    4) 최대 8개까지만 추가 가능
    5) 중복 태그 방지
    6) 태그 삭제 가능
    7) 폼 제출용 hidden input에 자동 저장
    8) 태그 선택시 tags목록에도 hover유지
    9) 태그 삭제시 hover유지 취소
    10) 태그도 최대 8개까지만 hover유지, alert띄움
*/
const input = document.querySelector("input[name='tag']");
const addBtn = document.querySelector(".add_tag_btn");
const outputArea = document.querySelector(".group_keyword_output");
const hiddenInput = document.querySelector("#group_keywords_hidden");
const tagLinks = document.querySelectorAll(".tags a"); // 아래 해시태그 리스트
const addedTags = new Set();
const MAX_TAGS = 8;
const HANGUL_REGEX = /^[가-힣]+$/;
// hidden input에 저장
function updateHiddenInput() {
    hiddenInput.value = Array.from(addedTags).join(",");
}
// 실제 태그 추가 함수 (중복, 제한 등 포함)
function addTag(tagText) {
    if (!tagText || addedTags.has(tagText)) return;
    if (addedTags.size >= MAX_TAGS) {
    alert("최대 8개의 태그만 추가할 수 있습니다.");
    return;
    }
    addedTags.add(tagText);
    const tag = document.createElement("div");
    tag.className = "added-tag";
    tag.textContent = tagText;
    const delBtn = document.createElement("span");
    delBtn.className = "tag-delete";
    delBtn.innerHTML = "&times;";
    // ⬇ 삭제 버튼 기능은 이 안에!
    delBtn.onclick = () => {
    addedTags.delete(tagText);
    tag.remove();
    updateHiddenInput();
    // ⬇ 아래 해시태그에서 hover 유지용 클래스도 제거
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
// input 기반 태그 추가 (한글 체크 포함)
function addTagFromInput() {
    const value = input.value.trim();
    const tagText = `#${value}`;
    if (!value) return;
    if (!HANGUL_REGEX.test(value)) {
    alert("한글만 입력 가능합니다.");
    return;
    }
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
    if (addedTags.size >= MAX_TAGS && !this.classList.contains("clicked")) {
        alert("최대 8개의 태그만 선택할 수 있습니다.");
        return;
    }
    addTag(tagText);
    this.classList.add("clicked");
    });
});


/* 그룹 비밀번호 관련 기능 추가:
    1) 공개여부-비공개 select 선택 시 비밀번호 설정부분 표시됨.
    2) 숫자 외 글자 입력시 차단(alert표시)
    3)  실시간 안내 UX (4~10자리만 입력 가능)
    4) 길이 초과 시 자르기 (11자리부터 미입력됨)
    5) 눈 아이콘 on/off 기능
*/
document.addEventListener("DOMContentLoaded", function () {
    const selectEl = document.getElementById("is_public");
    const pwRow = document.querySelector(".pw_hide");
    const pwInput = document.getElementById("group_pw");
    const toggleIcon = document.getElementById("togglePw");
    const pwMsg = document.getElementById("pw_message");

    // 공개/비공개 선택 시 비밀번호 입력칸 표시
    selectEl.addEventListener("change", function () {
    if (this.value === "1") {
        pwRow.style.display = "table-row";

        // DOM이 렌더링되고 난 후에 input 활성화를 위해 약간의 여유를 줌
        setTimeout(() => {
        pwInput.focus();
        pwInput.scrollIntoView({ behavior: "smooth", block: "center" });
        }, 50); // 50~100ms가 대부분 안정적
    } else {
        pwRow.style.display = "none";
        pwInput.value = "";
        pwInput.type = "password";
        toggleIcon.classList.remove("fa-eye");
        toggleIcon.classList.add("fa-eye-slash");
        pwMsg.textContent = "";
        pwMsg.className = "pw-message";
    }
    });

    // 숫자 외 입력 차단
    let alertShown = false;
    pwInput.addEventListener("keydown", function (e) {
    const allowed =
        (e.key >= "0" && e.key <= "9") ||
        ["Backspace", "Tab", "ArrowLeft", "ArrowRight", "Delete"].includes(e.key);

    if (!allowed) {
        e.preventDefault();

        if (!alertShown) {
        alertShown = true;
        alert("숫자만 입력 가능합니다.");
        setTimeout(() => (alertShown = false), 500);
        }
    }
    });

    // 실시간 유효성 검사
    pwInput.addEventListener("input", function () {
    const len = pwInput.value.length;

    if (len === 0) {
        pwMsg.textContent = "";
        pwMsg.className = "pw-message";
    } else if (len < 4) {
        pwMsg.textContent = "비밀번호는 4~10자리로 입력 가능합니다.";
        pwMsg.className = "pw-message invalid";
    } else {
        pwMsg.textContent = "사용 가능한 비밀번호입니다.";
        pwMsg.className = "pw-message valid";
    }

    // 혹시라도 maxlength 초과 입력 시 자동 자르기
    if (len > 10) {
        pwInput.value = pwInput.value.slice(0, 10);
    }
    });

    // 비밀번호 보기/숨기기 토글
    toggleIcon.addEventListener("click", function () {
    const isHidden = pwInput.type === "password";

    pwInput.type = isHidden ? "text" : "password";
    toggleIcon.classList.toggle("fa-eye-slash", !isHidden);
    toggleIcon.classList.toggle("fa-eye", isHidden);
    });
});


// 취소/완료 버튼 alert
document.addEventListener("DOMContentLoaded", function() {
    const cancelBtn = document.getElementById("group_button_1");
    const submitBtn = document.getElementById("group_button_2");
    // 취소 버튼 클릭 시
    cancelBtn.addEventListener("click", function() {
    const result = confirm("교환독서 메인페이지로 이동하시겠습니까?");
    if (result) {
        // 확인 누른 경우
        console.log("이동");
        window.location.href = "/shareMain/Share_Main/";
    } else {
        // 취소 누른 경우
        console.log("이동 취소");
    }
    });
    // 완료 버튼 클릭 시
    submitBtn.addEventListener("click", function() {
    if($('input[name="group_name"]').val().length<2){
        alert('그룹명을 입력하세요.');
        $('input[name="group_name"]').focus();
        return;
    }
    if($('textarea[name="description"]').val().length<2){
        alert('그룹 소개글을 입력하세요.');
        $('textarea[name="description"]').focus();
        return;
    }
    if($('select[name="is_public"]').val() === "1"){
        if($('input[name="password"]').val().length<4){
        alert('비밀번호를 입력하세요.');
        $('input[name="password"]').focus();
        return;
        }
    }
    addgroupFrm.submit();
    console.log("제줄 test");
    });
});