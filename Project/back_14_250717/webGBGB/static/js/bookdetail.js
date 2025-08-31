  // ========== 북마크 버튼 ==========
  function toggleBookmark(button) {
      const bookId = button.getAttribute('data-book-id');
      if (!bookId) {
          alert("book_id가 없습니다!");
          return;
      }

      let cToken = $('meta[name="csrf-token"]').attr('content');
      const icon = button.querySelector('i');
      if (!icon) {
          console.warn('아이콘 없음');
          return;
      }

      $.ajax({
          url: '/bookmark/create/',
          type: 'post',
          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': cToken },
          data: JSON.stringify({ book_id: bookId }),
          success: function(data) {
              if (data.bookmarked !== undefined) {
                  icon.classList.remove('fa-solid', 'fa-regular');
                  icon.classList.add(data.bookmarked ? 'fa-solid' : 'fa-regular');
                  button.classList.toggle('active', data.bookmarked);
              }
          },
          error: function() {
          }
      });

      // 애니메이션 효과는 성공 후에 처리하는 게 더 자연스러울 수 있습니다.
      icon.classList.add('fading-out');
      setTimeout(() => {
          icon.classList.remove('fading-out');
      }, 100);
  }

  // ========== 별점 바인딩 함수 (컨테이너별) ==========
  function bindStarRating(container) {
    const stars = container.querySelectorAll(".rating-stars-review .star");
    const input = container.querySelector("input[type='hidden'][name='rating']");
    const valSpan = container.querySelector(".caption-review .val");
    const textSpan = container.querySelector(".caption-review-badge span > span:first-child");
    let currentValue = parseInt(input?.value || "0");

    function updateStars(value) {
      stars.forEach((s, idx) => {
        s.classList.toggle("active", idx < value);
      });
      if (input) input.value = value;
      if (valSpan) valSpan.textContent = value;
      if (textSpan) textSpan.textContent = `5점 중 ${value}점`;
      currentValue = value;
    }

    stars.forEach((star, idx) => {
      const hoverValue = idx + 1;
      star.addEventListener("mouseenter", function () {
        stars.forEach((s, i) => {
          s.classList.toggle("active", i < hoverValue);
        });
        if (input) input.value = hoverValue;
        if (valSpan) valSpan.textContent = hoverValue;
        if (textSpan) textSpan.textContent = `5점 중 ${hoverValue}점`;
      });
      star.addEventListener("mouseleave", function () {
        updateStars(currentValue);
      });
      star.addEventListener("click", function () {
        const newValue = idx + 1;
        stars.forEach((s, i) => {
          const shouldFade = (i < currentValue && i >= newValue) || (i >= currentValue && i < newValue);
          if (shouldFade) s.classList.add("fading-out");
        });
        setTimeout(() => {
          updateStars(newValue);
          stars.forEach(s => s.classList.remove("fading-out"));
        }, 120);
      });
    });
    updateStars(currentValue);
  }
  
// ======================= 작성/수정 모달 폼 바인딩 =======================
function bindModalForm(modalId, formId, textareaId, ratingInputSelector, tagSelector, btnId) {
    const modal = document.getElementById(modalId);
    const form = document.getElementById(formId);
    const modalBtn = modal.querySelector(`#${btnId}`);
    const textarea = modal.querySelector(`#${textareaId}`);
    const ratingInput = modal.querySelector(ratingInputSelector);

    function setRating(value) {
        ratingInput.value = value;
        const stars = modal.querySelectorAll(".rating-stars-review .star");
        stars.forEach((s, idx) => s.classList.toggle("active", idx < value));
        const valSpan = modal.querySelector(".caption-review .val");
        const textSpan = modal.querySelector(".caption-review-badge span > span:first-child");
        if (valSpan) valSpan.textContent = value;
        if (textSpan) textSpan.textContent = `5점 중 ${value}점`;
        bindStarRating(modal)
    }

    function resetForm() {
        setRating(0);
        modal.querySelectorAll('.tag_wrap.size_lg .tag.active').forEach(tag => tag.classList.remove("active"));
        if (textarea) textarea.value = "";
        const counter = modal.querySelector(".byte_check .count");
        if (counter) counter.textContent = "0";
        // if (modalBtn) modalBtn.disabled = true;
        const tagInput = modal.querySelector("input[name='tag']");
        if (tagInput) tagInput.value = "";
    }

    function setFormData({ rating, tag, reviewText, imageUrls }) {
        if (typeof rating !== "undefined") setRating(parseInt(rating));
        if (tag) {
            modal.querySelectorAll('.tag_wrap.size_lg .tag').forEach(btn => {
                const tagText = btn.querySelector('.text')?.textContent.trim();
                btn.classList.toggle("active", tagText === tag);
            });
            const tagInput = modal.querySelector("input[name='tag']");
            if (tagInput) tagInput.value = tag;
        }
        if (textarea && typeof reviewText !== "undefined") {
            textarea.value = reviewText;
            const counter = modal.querySelector(".byte_check .count");
            if (counter) counter.textContent = reviewText.length;
        }
        checkFormValid();
        // 이미지 미리보기는 별도 관리
        if (modalId === "modifyModal" && typeof setModifyAttachedFiles === 'function' && Array.isArray(imageUrls)) {
            setModifyAttachedFiles(imageUrls);
            renderModifyFileList();
        }
    }

    function checkFormValid() {
        const ratingVal = parseInt(ratingInput?.value || "0");
        const ratingValid = ratingVal > 0;
        const tagSelected = modal.querySelector('.tag_wrap.size_lg .tag.active') !== null;
        const reviewLength = textarea?.value.trim().length || 0;
        const reviewValid = reviewLength >= 10;
        // if (modalBtn) modalBtn.disabled = !(ratingValid && tagSelected && reviewValid);
    }

    if (textarea) {
        textarea.addEventListener("input", () => {
            const len = textarea.value.length;
            const counter = modal.querySelector(".byte_check .count");
            if (counter) counter.textContent = len;
            checkFormValid();
        });
    }

    modal.querySelectorAll(".rating-stars-review .star").forEach(star => {
        star.addEventListener("click", () => checkFormValid());
    });

    modal.querySelectorAll('.tag_wrap.size_lg .tag').forEach(tag => {
        tag.addEventListener("click", () => {
            modal.querySelectorAll('.tag_wrap.size_lg .tag').forEach(btn => btn.classList.remove("active"));
            tag.classList.add("active");
            const tagInput = modal.querySelector("input[name='tag']");
            if (tagInput) tagInput.value = tag.querySelector('.text')?.textContent.trim();
            checkFormValid();
        });
    });

    return { resetForm, setFormData, checkFormValid, setRating };
}

// ======================= 수정 모달 이미지 미리보기 관리 (리팩토링) =======================
document.addEventListener('DOMContentLoaded', function () {
  const fileList = document.querySelector('.modify_file_list');
  const MAX_FILES = 3;

  let modifyAttachedFiles = [];

  function generateId() {
    return 'file_' + Math.random().toString(36).slice(2);
  }

  // DataTransfer를 이용해 input.files 동기화
  function syncInputFiles() {
    const fileInput = document.querySelector('input[type="file"][name="modify_review_image"]');
    if (!fileInput) return;
    const dt = new DataTransfer();
    modifyAttachedFiles.forEach(f => {
      if (f.file) dt.items.add(f.file);
    });
    fileInput.files = dt.files;
  }

  // 기존 이미지 hidden input 추가 함수
  function updateExistingImageInputs() {
    const container = document.getElementById('existingImagesInputs');
    if (!container) return;
    container.innerHTML = '';
    modifyAttachedFiles.forEach(fileData => {
      if (!fileData.file && fileData.url) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'existing_images';
        input.value = fileData.url;
        container.appendChild(input);
      }
    });
  }

  function updateModifyAttachVal() {
    const valElem = document.querySelector('.modify_file_attach_val .val');
    if (valElem) {
      valElem.textContent = modifyAttachedFiles.length;
    }
  }

  function createModifyBtnBox(attached = false, imgSrc = '', fileObj = null) {
    const id = generateId();

    const li = document.createElement('li');
    li.classList.add('list_item');
    li.innerHTML = `
      <span class="file_item ${attached ? 'attached' : ''}">
        <span class="btn_box">
          <input id="${id}" type="file" name="modify_review_image" multiple />
          <label for="${id}"><span class="hidden">첨부파일 추가</span></label>
          <span class="attach_img_box" style="display:${attached ? 'inline-block' : 'none'};">
            <span class="attach_img_view" style="background-image: url('${imgSrc}');"></span>
            <button class="btn_remove_img" type="button"><span class="hidden">첨부파일 삭제</span></button>
          </span>
        </span>
      </span>
    `;

    const input = li.querySelector('input[type="file"]');
    const removeBtn = li.querySelector('.btn_remove_img');
    const preview = li.querySelector('.attach_img_view');
    const attachBox = li.querySelector('.attach_img_box');
    const fileItem = li.querySelector('.file_item');

    // 새로 추가한 이미지(첨부) 처리
    if (!attached) {
      input.addEventListener('change', () => {
        const file = input.files[0];
        if (!file) return;

        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
        if (!allowedTypes.includes(file.type)) {
          alert('이미지 파일(JPG, PNG, GIF)만 업로드 가능합니다.');
          input.value = '';
          return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
          modifyAttachedFiles.push({ file: file, url: e.target.result });

          // 현재 btn_box를 attached로 변경
          fileItem.classList.add('attached');
          attachBox.style.display = 'inline-block';
          preview.style.backgroundImage = `url('${e.target.result}')`;

          // 미리보기 다시 그리기
          renderModifyFileList();
          syncInputFiles(); // 추가!
        };
        reader.readAsDataURL(file);
      });
    }

    removeBtn.addEventListener('click', () => {
      // 미리보기의 backgroundImage에서 url 추출
      const bgImage = preview.style.backgroundImage;
      const url = bgImage.slice(5, -2); // url('...')에서 ...만 추출

      // modifyAttachedFiles에서 해당 url을 가진 객체 찾기
      const idx = modifyAttachedFiles.findIndex(f => f.url === url);
      if (idx !== -1) {
        modifyAttachedFiles.splice(idx, 1);
        renderModifyFileList();
        syncInputFiles(); // 추가!
        return;
      }

      // 혹시 못 찾으면 attached별로 기존 로직도 실행
      if (attached) {
        const allItems = Array.from(fileList.querySelectorAll('.list_item'));
        const currentIndex = allItems.indexOf(li);
        const nextLi = li.nextElementSibling;
        const lastLi = allItems[allItems.length - 1];

        const hasRightEmptyDiv =
          nextLi &&
          !nextLi.querySelector('.file_item').classList.contains('attached');

        const lastIsEmpty =
          lastLi &&
          !lastLi.querySelector('.file_item').classList.contains('attached');

        if (hasRightEmptyDiv) {
          fileList.removeChild(li);
        } else {
          if (currentIndex === 0) {
            fileList.removeChild(li);
            if (!lastIsEmpty && modifyAttachedFiles.length < MAX_FILES) {
              fileList.appendChild(createModifyBtnBox(false, ''));
            }
          } else if (currentIndex === 1) {
            fileList.removeChild(li);
            if (!hasRightEmptyDiv && modifyAttachedFiles.length < MAX_FILES) {
              fileList.appendChild(createModifyBtnBox(false, ''));
            }
          } else if (currentIndex === 2) {
            fileItem.classList.remove('attached');
            preview.style.backgroundImage = '';
            attachBox.style.display = 'none';
            input.value = '';
          }
        }
        updateModifyAttachVal();
        updateExistingImageInputs();
        syncInputFiles(); // 추가!
      }
    });

    return li;
  }

  // 초기 이미지 세팅 함수 (예: 서버에서 받은 이미지 url 배열로 초기화)
  function setModifyAttachedFiles(imageUrls = []) {
    modifyAttachedFiles = imageUrls.map(url => ({ file: null, url }));
    renderModifyFileList();
    syncInputFiles(); // 추가!
  }

  // 리스트 렌더링
  function renderModifyFileList() {
    fileList.innerHTML = '';
    modifyAttachedFiles.forEach(fileData => {
      fileList.appendChild(createModifyBtnBox(true, fileData.url, fileData.file));
    });
    if (modifyAttachedFiles.length < MAX_FILES) {
      fileList.appendChild(createModifyBtnBox(false, ''));
    }
    updateModifyAttachVal();
    updateExistingImageInputs();
    syncInputFiles(); // 추가!
  }

  // 최초 렌더링
  fileList.innerHTML = '';
  fileList.appendChild(createModifyBtnBox(false, ''));
  updateModifyAttachVal();

  // 필요시 외부에서 setModifyAttachedFiles(imageUrls) 호출로 초기값 세팅 가능
  window.setModifyAttachedFiles = setModifyAttachedFiles;
  window.renderModifyFileList = renderModifyFileList;

  // 폼 submit 직전에 hidden input 갱신
  const form = document.getElementById('modifyForm');
  if (form) {
    form.addEventListener('submit', function () {
      updateExistingImageInputs();
      syncInputFiles(); // 추가!
    });
  }
});

// ========== DOMContentLoaded에서 모든 기능 바인딩 ==========
document.addEventListener("DOMContentLoaded", () => {
    // ========== 댓글/답글 글자수 체크 ==========
    document.querySelectorAll('.form_textarea').forEach(textarea => {
        textarea.addEventListener('input', () => {
            const count = textarea.closest('.reply_write_area, .modal')?.querySelector('.byte_check .count');
            if (count) count.textContent = textarea.value.length;
        });
    });

    // ========== 댓글 펼치기/접기 ==========
    document.querySelectorAll('.comment_item').forEach(item => {
        const moreBtn = item.querySelector('.btn_more_body');
        if (!moreBtn) return;
        moreBtn.style.display = item.classList.contains('overflow') ? 'block' : 'none';

        moreBtn.addEventListener('click', () => {
            const isActive = item.classList.toggle('active');
            moreBtn.classList.toggle('active', isActive);
            moreBtn.querySelector('.text').textContent = isActive ? '접기' : '펼치기';
            const icon = moreBtn.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-circle-arrow-up', isActive);
                icon.classList.toggle('fa-circle-arrow-down', !isActive);
            }
            const thumb = item.querySelector('.comment_thumb_box');
            const swiper = item.querySelector('.comment_swiper_wrap');
            if (thumb && swiper) {
                thumb.style.display = isActive ? 'none' : 'block';
                swiper.style.display = isActive ? 'block' : 'none';
            }
        });
    });

    // ========== 이미지 썸네일 클릭 시 Swiper 보기 ==========
    document.querySelectorAll('.comment_thumb_box').forEach(box => {
      box.addEventListener('click', () => {
        const item = box.closest('.comment_item');
        if (!item) return;

        const thumb = item.querySelector('.comment_thumb_box');
        const swiper = item.querySelector('.comment_swiper_wrap');
        const moreBtn = item.querySelector('.btn_more_body');
        const moreBtnText = moreBtn ? moreBtn.querySelector('.text') : null;
        const icon = moreBtn ? moreBtn.querySelector('i') : null;

        // 이미 열려 있으면 닫기
        if (item.classList.contains('active')) {
          item.classList.remove('overflow', 'active');
          if (thumb) thumb.style.display = 'block';
          if (swiper) swiper.style.display = 'none';
          if (moreBtn) moreBtn.classList.remove('active');

        } else {
          // 닫혀 있으면 열기
          item.classList.add('overflow', 'active');
          if (thumb) thumb.style.display = 'none';
          if (swiper) swiper.style.display = 'block';
          if (moreBtn) moreBtn.classList.add('active');
          if (moreBtnText) moreBtnText.textContent = '접기';
          if (icon) {
            icon.classList.add('fa-circle-arrow-up');
            icon.classList.remove('fa-circle-arrow-down');
          }
        }
      });
    });

    // ========== 좋아요 ==========
    document.querySelectorAll('.btn_like').forEach(likeBtn => {
        likeBtn.addEventListener('click', function () {
            if (likeBtn.classList.contains('processing')) return;
            likeBtn.classList.add('processing');
            const reviewId = likeBtn.getAttribute('data-review-id');
            let cToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            const countEl = this.querySelector('.text');
            const icon = this.querySelector('i');

            $.ajax({
                url: '/review/like/',
                type: 'post',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': cToken },
                data: JSON.stringify({ review_id: reviewId }),
                success: function (data) {
                    if (data.likes !== undefined) {
                        countEl.textContent = data.likes;
                    }
                    if (data.liked !== undefined) {
                        likeBtn.classList.toggle('liked', data.liked);
                        icon?.classList.toggle('fa-solid', data.liked);
                        icon?.classList.toggle('fa-regular', !data.liked);
                    }
                },
                complete: function () {
                    likeBtn.classList.remove('processing');
                }
            });
        });
    });

    // ========== 답글달기 토글 ==========
    $(document).on('click', '.btn_reply', function () {
        const $commentItem = $(this).closest('.comment_item');
        $commentItem.find('.reply_wrap').first().toggle();
    });

    // ========== 댓글/답글 폼 유효성 검사 ==========
    document.querySelectorAll('.reply_wrap').forEach(area => {
      const replyBtn = area.querySelector(".reply_btn");
      const textarea = area.querySelector(".reply_comments");
      const countSpan = area.querySelector('.reply_byte_check .count');
      const form = area.querySelector(".replyForm");

      function checkFormValid() {
          if (!textarea || !replyBtn) return;
          const reviewLength = textarea.value.trim().length;
          const reviewValid = reviewLength >= 1;
          replyBtn.disabled = !reviewValid;
          if (countSpan) countSpan.textContent = reviewLength;
      }

      if (textarea) {
          textarea.addEventListener("input", checkFormValid);
          checkFormValid();
      }
        checkFormValid();

        function resetReplyForm() {
            textarea.value = "";
            if (countSpan) countSpan.textContent = "0";
            replyBtn.disabled = true;
        }
      if (replyBtn) {
          replyBtn.addEventListener("click", () => {
              if (form) form.submit();
              resetReplyForm();
          });
      }
    });

    // ========== 작성/수정 모달 바인딩 ==========
    const reviewModalApi = bindModalForm(
        "reviewModal", "reviewForm", "review_comments",
        "input[name='rating']", "input[name='tag']", "review_btn"
    );
    const modifyModalApi = bindModalForm(
        "modifyModal", "modifyForm", "modify_comments",
        "input[name='rating']", "input[name='tag']", "modify_btn"
    );

    // ========== 작성 모달 열기/닫기 ==========
    document.getElementById("openReviewBtn")?.addEventListener('click', () => {
        const memberId = document.getElementById("openReviewBtn").dataset.memberId;
        if (!memberId || memberId === "None") {
            alert("로그인 후 이용 가능합니다.");
            window.location.href = "/member/login/";
            return;
        }
        document.getElementById("reviewModal")?.classList.add('active');
        reviewModalApi.resetForm();
    });
    document.getElementById("closeReviewBtn")?.addEventListener('click', () => {
        document.getElementById("reviewModal")?.classList.remove('active');
        reviewModalApi.resetForm();
    });
    // ========== 수정 모달 열기/닫기 ==========
    document.querySelectorAll('.modifyReviewBtn').forEach(btn => {
      btn.addEventListener('click', function() {
        let reviewData = {};
        try { reviewData = JSON.parse(btn.dataset.review); }
        catch (err) { alert("리뷰 데이터 파싱 오류!"); return; }
        const modal = document.getElementById("modifyModal");
        modal?.classList.add('active');
        const imageUrls = btn.dataset.images
          ? btn.dataset.images.split(',').filter(Boolean)
          : [];
        modifyModalApi.resetForm();
        modifyModalApi.setFormData({
          rating: reviewData.rating,
          tag: reviewData.tag,
          reviewText: reviewData.content,
          imageUrls: imageUrls
        });
        // 기존 이미지 세팅
        if (typeof window.setModifyAttachedFiles === 'function') {
          window.setModifyAttachedFiles(imageUrls);
        }
        const reviewIdInput = modal.querySelector("#modal_review_id");
        if (reviewIdInput) reviewIdInput.value = reviewData.review_id;
      });
    });
    document.getElementById("closeModifyBtn")?.addEventListener('click', () => {
        document.getElementById("modifyModal")?.classList.remove('active');
        modifyModalApi.resetForm();
    });
    // ========== esc로 모달 닫기 ==========
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') {
            document.getElementById("reviewModal")?.classList.remove('active');
            reviewModalApi.resetForm();
            document.getElementById("modifyModal")?.classList.remove('active');
            modifyModalApi.resetForm();
        }
    });

    // ========== 작성/수정 모달 등록 버튼 ==========
    document.getElementById('review_btn')?.addEventListener('click', function(e) {
        const modal = document.getElementById("reviewModal");
        const rating = modal.querySelector("input[name='rating']").value;
        const tag = modal.querySelector("input[name='tag']").value;
        const textarea = modal.querySelector("#review_comments");
        const reviewText = textarea ? textarea.value.trim() : "";

        if (!rating || rating === "0" || !tag || reviewText.length < 10) {
            alert("별점, 태그, 리뷰 10글자 이상을 모두 입력해야 합니다.");
            return;
        }
        document.getElementById('reviewForm').submit();
        alert("리뷰가 등록되었습니다.")
      });
      
      document.getElementById('modify_btn')?.addEventListener('click', function(e) {
        const modal = document.getElementById("modifyModal");
        const rating = modal.querySelector("input[name='rating']").value;
        const tag = modal.querySelector("input[name='tag']").value;
        const textarea = modal.querySelector("#modify_comments");
        const reviewText = textarea ? textarea.value.trim() : "";
        
        if (!rating || rating === "0" || !tag || reviewText.length < 10) {
          alert("별점, 태그, 리뷰 10글자 이상을 모두 입력해야 합니다.");
          return;
        }
        document.getElementById('modifyForm').submit();
        alert("리뷰가 수정되었습니다.")
    });


    // ========== 수정 모달 이미지 최초 렌더 ==========
    renderModifyFileList();
});

  // ========== 모달 팝업 내 사진 추가 ==========
  document.addEventListener('DOMContentLoaded', function () {
    const fileList = document.querySelector('.file_list');
    const MAX_FILES = 3;

    let attachedFiles = [];

    function generateId() {
      return 'file_' + Math.random().toString(36).slice(2);
    }

    function updateAttachVal() {
      const valElem = document.querySelector('.file_attach_val .total');
      if (valElem) {
        valElem.textContent = ` / ${MAX_FILES}`;
        const currentValElem = valElem.previousElementSibling;
        if (currentValElem && currentValElem.classList.contains('val')) {
          currentValElem.textContent = attachedFiles.length;
        }
      }
    }

    function createBtnBox(attached = false, imgSrc = '') {
      const id = generateId();

      const li = document.createElement('li');
      li.classList.add('list_item');
      li.innerHTML = `
        <span class="file_item ${attached ? 'attached' : ''}">
          <span class="btn_box">
            <input id="${id}" type="file" name="review_image" multiple/>
            <label for="${id}"><span class="hidden">첨부파일 추가</span></label>
            <span class="attach_img_box" style="display:${attached ? 'inline-block' : 'none'};">
              <span class="attach_img_view" style="background-image: url('${imgSrc}');"></span>
              <button class="btn_remove_img" type="button"><span class="hidden">첨부파일 삭제</span></button>
            </span>
          </span>
        </span>
      `;

      const input = li.querySelector('input[type="file"]');
      const removeBtn = li.querySelector('.btn_remove_img');
      const preview = li.querySelector('.attach_img_view');
      const attachBox = li.querySelector('.attach_img_box');
      const fileItem = li.querySelector('.file_item');

      input.addEventListener('change', () => {
        const file = input.files[0];
        if (!file) return;

        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];

        if (!allowedTypes.includes(file.type)) {
          alert('이미지 파일(JPG, PNG, GIF)만 업로드 가능합니다.');
          input.value = '';
          return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
          const imgUrl = e.target.result;
          attachedFiles.push(imgUrl);

          // 1. 현재 btn_box를 attached로 변경
          fileItem.classList.add('attached');
          attachBox.style.display = 'inline-block';
          preview.style.backgroundImage = `url('${imgUrl}')`;

          // 2. 필요한 경우 오른쪽에 새 btn_box 추가
          const listItems = fileList.querySelectorAll('.list_item');
          if (attachedFiles.length < MAX_FILES) {
            const lastItem = listItems[listItems.length - 1];
            if (lastItem && lastItem === li) {
              const newBox = createBtnBox(false, '');
              fileList.appendChild(newBox);
            }
          }

          updateAttachVal();
        };
        reader.readAsDataURL(file);
      });

      removeBtn.addEventListener('click', () => {
        const bgImage = preview.style.backgroundImage;
        const url = bgImage.slice(5, -2);
        const index = attachedFiles.indexOf(url);
        if (index !== -1) attachedFiles.splice(index, 1);

        const allItems = Array.from(fileList.querySelectorAll('.list_item'));
        const currentIndex = allItems.indexOf(li);
        const nextLi = li.nextElementSibling;
        const lastLi = allItems[allItems.length - 1];

        // 오른쪽에 빈 사진추가 div 있는지 체크
        const hasRightEmptyDiv =
          nextLi &&
          !nextLi.querySelector('.file_item').classList.contains('attached');

        // 맨 끝이 빈 사진 추가 div인지 체크
        const lastIsEmpty =
          lastLi &&
          !lastLi.querySelector('.file_item').classList.contains('attached');

        if (hasRightEmptyDiv) {
          // 오른쪽에 빈 div 있으면 무조건 자기 삭제만
          fileList.removeChild(li);
        } else {
          if (currentIndex === 0) {
            // 첫 번째 div 삭제
            fileList.removeChild(li);
            // 맨 끝에 사진 추가 div 없으면 새로 추가
            if (!lastIsEmpty && attachedFiles.length < MAX_FILES) {
              fileList.appendChild(createBtnBox(false, ''));
            }
          } else if (currentIndex === 1) {
            // 두 번째 div 삭제
            fileList.removeChild(li);
            // 오른쪽에 빈 div 없으면 맨 끝에 새로 추가
            if (!hasRightEmptyDiv && attachedFiles.length < MAX_FILES) {
              fileList.appendChild(createBtnBox(false, ''));
            }
          } else if (currentIndex === 2) {
            // 세 번째 div: attached 제거, 내용 비우기
            fileItem.classList.remove('attached');
            preview.style.backgroundImage = '';
            attachBox.style.display = 'none';
            input.value = '';
          }
        }

        updateAttachVal();
      });


      return li;
    }

    // 초기 1개 빈 박스 생성
    fileList.innerHTML = '';
    fileList.appendChild(createBtnBox(false, ''));
    updateAttachVal();
  });

  // ========== 답글 수정 버튼 클릭 시 ==========
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('reply-edit-btn')) {
      e.preventDefault();
      const replyId = e.target.dataset.replyId;
      const replyItem = document.getElementById(replyId);

      // 기존 답글 내용 영역
      const replyContents = replyItem.querySelector('.reply_contents');
      const originalHtml = replyContents.innerHTML;

      // 기존 답글 텍스트
      const originalText = replyItem.querySelector('.reply_text').textContent.trim();

      // 수정폼 HTML 생성 (form 태그로 감싸기)
      const modifyFormHtml = `
        <form class="replymodifyForm" method="post" action="/reply/modify/${replyId}/">
          <input type="hidden" name="csrfmiddlewaretoken" value="${getCSRFToken()}">
          <div class="modify_reply_write_area active">
            <div class="modify_byte_check_wrap">
              <textarea class="form_textarea reply_comments" name="replymodifycontent" title="답글 입력" placeholder="1000자 이내로 입력해주세요." maxlength="1000">${originalText}</textarea>
              <div class="modify_byte_check_footer">
                <div class="modify_reply_byte_check">
                  <span class="count">${originalText.length}</span>
                  <span class="total">1000</span>
                </div>
              </div>
            </div>
            <div class="modify_btn_wrap_home">
              <div class="modify_btn_wrap">
                <button class="modify_btn_xs btn_primary cancle_btn" type="button" style="background: #636363; color: #fafafa;">
                  <span class="modify_text" style="font-weight: 500;">취소</span>
                </button>
                <button class="modify_btn_xs btn_primary reply_btn" type="submit" disabled>
                  <span class="modify_text" style="font-weight: 500;">등록</span>
                </button>
              </div>
            </div>
          </div>
        </form>
      `;

      // reply_contents 부분만 교체
      replyContents.innerHTML = modifyFormHtml;

      // 이벤트 바인딩
      setTimeout(() => {
        const textarea = replyContents.querySelector('textarea.reply_comments');
        const regBtn = replyContents.querySelector('.reply_btn');
        const cancelBtn = replyContents.querySelector('.cancle_btn');
        const countSpan = replyContents.querySelector('.count');
        const form = replyContents.querySelector(".replymodifyForm");

        textarea.addEventListener('input', function() {
          const val = textarea.value.trim();
          regBtn.disabled = val.length < 1;
          regBtn.classList.toggle('disabled', val.length < 1);
          countSpan.textContent = val.length;
        });

        cancelBtn.addEventListener('click', function() {
          replyContents.innerHTML = originalHtml;
        });

        // 폼 제출은 자동 (submit 버튼 클릭 시)
        // 필요하면 form.addEventListener('submit', ...)에서 추가 검증 가능
      }, 0);
    }
  });

  // ==================== CSRF 토큰 함수 ====================
  function getCSRFToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }
    return '';
  }

  document.addEventListener("DOMContentLoaded", function() {
  document.querySelectorAll('.btn_view_img').forEach(btn => {
    btn.addEventListener('click', function() {
      const url = btn.getAttribute('data-img-url');
      if (url) window.open(url, '_blank');
    });
  });
});

