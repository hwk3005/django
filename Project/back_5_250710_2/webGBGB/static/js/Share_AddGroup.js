document.addEventListener("DOMContentLoaded", function () {
    // =========================
    // 책 검색 모달 관련
    // =========================
    const modal = document.getElementById("book_search_modal");
    const overlay = modal.querySelector(".modal_overlay");
    const closeBtn = modal.querySelector(".modal_close");
    const input = document.getElementById("book_search_input_modal");
    const searchBtn = document.getElementById("modal_search_btn");
    const results = document.querySelector(".modal_results");
    const selectedDisplay = document.getElementById("selected-book-display");

    // form의 hidden input 요소들
    const inputTitle = document.getElementById("id_book_title");
    const inputAuthor = document.getElementById("id_book_author");
    const inputCover = document.getElementById("id_book_cover");
    const inputISBN = document.getElementById("id_book_isbn");

    // 모달 열기
    function openModal() {
        modal.style.display = "block";
        input.focus();
        results.innerHTML = "";
    }
    // 모달 닫기
    function closeModal() {
        modal.style.display = "none";
        results.innerHTML = "";
        input.value = "";
    }
    // 모달 열기 트리거
    document.addEventListener("click", function (e) {
        if (e.target.closest("#book_search_trigger")) {
            e.preventDefault();
            openModal();
        }
    });
    // 모달 닫기
    overlay.addEventListener("click", closeModal);
    closeBtn.addEventListener("click", function (e) {
        e.preventDefault();
        closeModal();
    });

    // 책 검색
    searchBtn.addEventListener("click", function () {
        const query = input.value.trim();
        if (!query) {
            results.innerHTML = "<p>검색어를 입력해주세요.</p>";
            return;
        }
        fetch(`${AJAX_SEARCH_URL}?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                const books = data.books || [];
                if (books.length === 0) {
                    results.innerHTML =
                        "<p style='text-align:center; padding: 20px; font-size:16px; color:#636363;'>검색 결과가 없습니다.</p>";
                    return;
                }
                results.innerHTML = books.map(book => `
                  <div class="modal_result"
                       data-title="${book.title}"
                       data-author="${book.author}"
                       data-cover="${book.cover}"
                       data-isbn="${book.isbn}">
                    <div class="modal_book_item">
                      <img src="${book.cover}" alt="${book.title}" />
                    </div>
                    <div class="modal_book_info">
                      <h3>${book.title}</h3>
                      <p><strong>저자:</strong> ${book.author}</p>
                      <p><strong>출판사:</strong> ${book.publisher}</p>
                    </div>
                    <div class="modal_book_select">
                      <button type="button" class="modal_book_select_btn">선택</button>
                    </div>
                  </div>
                `).join("");
            })
            .catch(error => {
                console.error("책 검색 오류:", error);
                results.innerHTML = "<p>검색 중 오류가 발생했습니다.</p>";
            });
    });
    input.addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            searchBtn.click();
        }
    });

    // 책 선택 시 - form hidden input에 삽입 + UI 표시
    results.addEventListener("click", function (e) {
        if (e.target.classList.contains("modal_book_select_btn")) {
            const bookDiv = e.target.closest(".modal_result");
            const title = bookDiv.dataset.title;
            const author = bookDiv.dataset.author;
            const cover = bookDiv.dataset.cover;
            const isbn = bookDiv.dataset.isbn;

            // 콘솔에 선택한 책 정보 출력!
            console.log("선택한 책:", title, author, cover, isbn);

            // hidden input에 값 넣기
            inputTitle.value = title;
            inputAuthor.value = author;
            inputCover.value = cover;
            inputISBN.value = isbn;

            // UI에 선택된 책 표시
            selectedDisplay.innerHTML = `
                <a href="#" id="book_search_trigger">
                <div class="selected_book_img_js">
                  <div class="tooltip_wrapper">
                    <img src="${cover}" alt="${title}">
                    <div class="custom_tooltip">변경<br></div>
                  </div>
                </div>
                </a>
                <div class="selected_book_text">
                    <span>${title}</span>
                    <p>${author}</p>
                </div>
            `;
            closeModal();
        }
    });

    // =========================
    // 해시태그 기능
    // =========================
    const tagInput = document.querySelector("input[name='tag_input']");
    const addBtn = document.querySelector(".add_tag_btn");
    const outputArea = document.querySelector(".group_keyword_output");
    const hiddenInput = document.querySelector("#group_keywords_hidden");
    const tagLinks = document.querySelectorAll(".tags a"); // 추천 해시태그 리스트
    const addedTags = new Set();
    const MAX_TAGS = 8;
    const HANGUL_REGEX = /^[가-힣]+$/;

    function updateHiddenInput() {
        hiddenInput.value = Array.from(addedTags).join(",");
    }

    function addTag(tagText) {
        if (!tagText || addedTags.has(tagText)) return;
        if (addedTags.size >= MAX_TAGS) {
            alert("최대 8개의 태그만 추가할 수 있습니다.");
            return;
        }
        addedTags.add(tagText);

        // 태그 UI 생성
        const tag = document.createElement("div");
        tag.className = "added-tag";
        tag.textContent = tagText;

        // 삭제 버튼
        const delBtn = document.createElement("span");
        delBtn.className = "tag-delete";
        delBtn.innerHTML = "&times;";
        delBtn.onclick = () => {
            addedTags.delete(tagText);
            tag.remove();
            updateHiddenInput();
            // 추천 해시태그 hover 해제
            tagLinks.forEach(link => {
                if (link.textContent.trim() === tagText) {
                    link.classList.remove("clicked");
                }
            });
        };
        tag.appendChild(delBtn);
        outputArea.appendChild(tag);

        // 추천 해시태그 hover 유지
        tagLinks.forEach(link => {
            if (link.textContent.trim() === tagText) {
                link.classList.add("clicked");
            }
        });

        updateHiddenInput();
    }

    function addTagFromInput() {
        const value = tagInput.value.trim();
        if (!value) return;
        if (!HANGUL_REGEX.test(value)) {
            alert("한글만 입력 가능합니다.");
            tagInput.value = "";
            return;
        }
        const tagText = `#${value}`;
        addTag(tagText);
        tagInput.value = "";
    }
    // 해시태그-직접입력-Enter
    tagInput.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            e.preventDefault();
            addTagFromInput();
        }
    });
    // 해시태그-직접입력-button
    addBtn.addEventListener("click", addTagFromInput);

    tagLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const tagText = this.textContent.trim();
            if (addedTags.has(tagText)) {
                // 이미 추가된 태그라면 hover만 유지
                this.classList.add("clicked");
                return;
            }
            if (addedTags.size >= MAX_TAGS) {
                alert("최대 8개의 태그만 선택할 수 있습니다.");
                return;
            }
            addTag(tagText);
            this.classList.add("clicked");
        });
    });

    // =========================
    // 그룹 비밀번호 관련
    // =========================
    const selectEl = document.getElementById("is_public");
    const pwRow = document.querySelector(".pw_hide");
    const pwInput = document.getElementById("group_pw");
    const toggleIcon = document.getElementById("togglePw");
    const pwMsg = document.getElementById("pw_message");

    selectEl.addEventListener("change", function () {
        if (this.value === "1") {
            pwRow.style.display = "table-row";
            setTimeout(() => {
                pwInput.focus();
                pwInput.scrollIntoView({ behavior: "smooth", block: "center" });
            }, 50);
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
        if (len > 10) {
            pwInput.value = pwInput.value.slice(0, 10);
        }
    });

    toggleIcon.addEventListener("click", function () {
        const isHidden = pwInput.type === "password";
        pwInput.type = isHidden ? "text" : "password";
        toggleIcon.classList.toggle("fa-eye-slash", !isHidden);
        toggleIcon.classList.toggle("fa-eye", isHidden);
    });

    // =========================
    // 취소/완료 버튼 & 폼 유효성 검사
    // =========================
    const cancelBtn = document.getElementById("group_button_1");
    const form = document.getElementById("addgroupFrm");
    const groupNameInput = form.querySelector('input[name="group_name"]');
    const descInput = form.querySelector('textarea[name="description"]');
    // 완료 버튼은 type="submit"이므로, submit 이벤트에서 처리

    // 취소 버튼
    cancelBtn.addEventListener("click", function() {
        if (confirm("교환독서 메인페이지로 이동하시겠습니까?")) {
            window.location.href = "/shareMain/Share_Main/";
        }
    });

    // 폼 제출 유효성 검사 (책/그룹명/소개/비밀번호)
    form.addEventListener("submit", function(e) {
        // 그룹명
        if (!groupNameInput.value.trim() || groupNameInput.value.trim().length < 2) {
            alert("그룹명을 2글자 이상 입력하세요.");
            groupNameInput.focus();
            e.preventDefault();
            return false;
        }
        // 소개글
        if (!descInput.value.trim() || descInput.value.trim().length < 2) {
            alert("그룹 소개글을 2글자 이상 입력하세요.");
            descInput.focus();
            e.preventDefault();
            return false;
        }
        // 책 선택
        if (!inputTitle.value.trim()) {
            alert("책을 선택해주세요.");
            const trigger = document.getElementById("book_search_trigger");
            if (trigger) {
                trigger.focus();
                trigger.scrollIntoView({behavior: "smooth", block: "center"});
            }
            e.preventDefault();
            return false;
        }
        // 비공개 시 비밀번호
        if (selectEl.value === "1") {
            if (!pwInput.value.trim() || pwInput.value.trim().length < 4) {
                alert("비공개 그룹은 4자리 이상의 비밀번호를 입력해야 합니다.");
                pwInput.focus();
                e.preventDefault();
                return false;
            }
        }
        // 해시태그 8개 초과 방지 (혹시나 직접 조작 방지)
        if (addedTags.size > MAX_TAGS) {
            alert("최대 8개의 태그만 추가할 수 있습니다.");
            e.preventDefault();
            return false;
        }
        // 통과 시 제출
    });
});
