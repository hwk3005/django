// 1) DOMContentLoaded → 초기 설정: 메뉴 닫기, 좋아요·댓글
document.addEventListener('DOMContentLoaded', () => {
  // 열린 메뉴 모두 닫기
  document.querySelectorAll('.settings-menu, .reply-settings-menu').forEach(m => m.remove());

  // 각 포스트마다 좋아요·댓글 버튼에 카운트 스팬 없으면 추가
  document.querySelectorAll('.post').forEach(post => {
    // 좋아요 버튼 (comment_footer 영역)
    const likeBtn = post.querySelector('.comment_footer .btn_like');
    if (likeBtn && !likeBtn.querySelector('.text')) {
      const span = document.createElement('span');
      span.className = 'text';
      span.textContent = '0';
      likeBtn.appendChild(span);
    }
    // 댓글 버튼
    const replyBtn = post.querySelector('.comment_footer .btn_reply');
    if (replyBtn && !replyBtn.querySelector('.count')) {
      const span = document.createElement('span');
      span.className = 'count';
      // 초기값: 이미 달린 댓글 수
      span.textContent = post.querySelectorAll('.reply_item:not(.nested-reply-item)').length; // 최상위 댓글만 카운트
      replyBtn.appendChild(span);
    }
    // 기존 댓글에 대댓글 영역 초기화 및 대댓글 수 업데이트
    post.querySelectorAll('.reply_item').forEach(replyItem => {
      // 이미 nested-reply-section이 있는 경우는 추가하지 않음
      if (!replyItem.querySelector('.nested-reply-section')) {
        addNestedReplySection(replyItem);
      }
      updateNestedReplyCount(replyItem); // 대댓글 수 초기화
    });
  });
});

// 2) 이벤트 위임: 좋아요·댓글·메뉴·댓글등록 처리
document.addEventListener('click', function(e) {
  const feedBtn = e.target.closest('.btn_setting');
  if (feedBtn) {
    e.stopPropagation();
    toggleMenu(
      feedBtn,
      '<button class="edit-post">수정</button><button class="delete-post">삭제</button>',
      'settings-menu'
    );
    return;
  }
  // 1) 피드 수정 버튼 클릭
  if (e.target.matches('.edit-post')) {
    e.stopPropagation();
    const post = e.target.closest('.post');
    const contentEl = post.querySelector('.post-contents');

    const imageHTML = Array
      .from(contentEl.querySelectorAll('img'))
      .map(img => img.outerHTML)
      .join('');

    const newText = prompt('게시글을 수정하세요:', contentEl.textContent.trim());
    if (newText !== null) {
      contentEl.innerHTML = imageHTML + newText;
    }
    document.querySelectorAll('.settings-menu').forEach(m => m.remove());
    return;
  }

  // 피드 “삭제” 클릭
  if (e.target.matches('.delete-post')) {
    e.stopPropagation();
    const post = e.target.closest('.post');
    if (confirm('정말 이 게시글을 삭제하시겠습니까?')) {
      post.remove();
    }
    return;
  }


  // 2-1) 피드 좋아요 클릭
  const feedLike = e.target.closest('.comment_footer .btn_like');
  if (feedLike) {
    e.stopPropagation();
    const icon = feedLike.querySelector('i');
    icon?.classList.replace('fa-regular', 'fa-solid');
    let badge = feedLike.querySelector('.text');
    if (!badge) {
      badge = document.createElement('span');
      badge.className = 'text';
      feedLike.appendChild(badge);
    }
    badge.textContent = String((parseInt(badge.textContent, 10) || 0) + 1);
    return;
  }

  // 2-2) 피드 댓글 버튼 클릭 → 댓글창 토글 + 댓글 수 갱신
  const feedReply = e.target.closest('.comment_footer .btn_reply');
  if (feedReply) {
    e.stopPropagation();
    const post = feedReply.closest('.post');
    const wrap = post.querySelector('.reply_wrap');
    wrap && wrap.classList.toggle('active');
    updateCommentCount(post);
    return;
  }

  // 2-3) 댓글 등록 (reply_wrap 내 .reply_btn)
  const postReplyBtn = e.target.closest('.reply_btn');
  if (postReplyBtn) {
    const post = postReplyBtn.closest('.post');
    const wrap = post.querySelector('.reply_wrap');
    // 대댓글 입력창의 textarea를 찾거나, 일반 댓글 입력창의 textarea를 찾음
    const ta = postReplyBtn.classList.contains('nested-reply-btn')
                 ? postReplyBtn.closest('.nested-reply-write-area').querySelector('.nested-reply-textarea')
                 : wrap.querySelector('#reply_textarea');

    const text = ta.value.trim();
    if (!text) return;

    // 대댓글 버튼인지 확인
    const isNestedReply = postReplyBtn.classList.contains('nested-reply-btn');
    if (isNestedReply) {
      const parentReplyItem = postReplyBtn.closest('.reply_item');
      if (parentReplyItem) {
        addNestedReply(parentReplyItem, text);
        ta.value = ''; // 입력창 비우기
        // 대댓글 등록 후 버튼 비활성화
        postReplyBtn.classList.add('disabled');
        return;
      }
    } else {
      // 일반 댓글 등록
      const item = createReplyItem(text);
      wrap.querySelector('.reply_list').appendChild(item);
      addNestedReplySection(item); // 새로 생성된 댓글에 대댓글 영역 추가
      ta.value = ''; // 입력창 비우기
      updateCommentCount(post);
      return;
    }
  }

  // 2-4) 댓글 “⋯” 메뉴 토글
  const commentMenuBtn = e.target.closest('.btn_reply_setting');
  if (commentMenuBtn) {
    e.stopPropagation();
    toggleMenu(
      commentMenuBtn,
      `<button class="edit-reply">수정</button><button class="delete-reply">삭제</button>`,
      'reply-settings-menu'
    );
    return;
  }

  // 2-5) 댓글 수정
  if (e.target.matches('.edit-reply')) {
    const item = e.target.closest('.reply_item');
    const contentEl = item.querySelector('.reply_content');
    const newText = prompt('댓글을 수정하세요:', contentEl.textContent.trim());
    if (newText !== null) contentEl.textContent = newText;
    closeAllReplyMenus();
    return;
  }

  // 2-6) 댓글 삭제
  if (e.target.matches('.delete-reply')) {
    if (confirm('댓글을 삭제하시겠습니까?')) {
      const item = e.target.closest('.reply_item');
      const post = item.closest('.post'); // 상위 게시글 찾기
      const isNested = item.classList.contains('nested-reply-item');

      // 대댓글인 경우 부모 댓글의 대댓글 수를 업데이트
      if (isNested) {
        const parentReplyList = item.closest('.nested-reply-list');
        if (parentReplyList) {
          const parentReplyItem = parentReplyList.closest('.reply_item');
          item.remove();
          if (parentReplyItem) {
            updateNestedReplyCount(parentReplyItem);
          }
        }
      } else {
        item.remove();
        updateCommentCount(post); // 최상위 댓글만 카운트 업데이트
      }
    }
    return;
  }

  // 2-7) 외부 클릭 시 메뉴 닫기
  if (!e.target.closest('.settings-menu')) {
    document.querySelectorAll('.settings-menu').forEach(m => m.remove());
  }
  if (!e.target.closest('.reply-settings-menu')) {
    document.querySelectorAll('.reply-settings-menu').forEach(m => m.remove());
  }

  // 2-8) 대댓글 토글 버튼 클릭 (reply_item 내의 말풍선 아이콘)
  const toggleNestedReplyBtn = e.target.closest('.btn_toggle_nested_reply');
  if (toggleNestedReplyBtn) {
    e.stopPropagation();
    const replyItem = toggleNestedReplyBtn.closest('.reply_item');
    const nestedReplySection = replyItem.querySelector('.nested-reply-section');
    if (nestedReplySection) {
      nestedReplySection.classList.toggle('active'); // active 클래스로 표시/숨기기
      if (nestedReplySection.classList.contains('active')) {
        // 활성화될 때 textarea에 포커스
        nestedReplySection.querySelector('.nested-reply-textarea').focus();
      }
    }
    return;
  }

});

// 3) 댓글 아이템 생성 (원본 디자인 그대로)
function createReplyItem(text) {
  const now = new Date();
  const date = `${now.getFullYear()}.${String(now.getMonth()+1).padStart(2,'0')}.${String(now.getDate()).padStart(2,'0')}`;
  const time = now.toTimeString().slice(0,5);
  const item = document.createElement('div');
  item.className = 'reply_item';
  item.innerHTML = `
    <div class="reply_header" style="width:100%">
      <div class="reply_wrapper">
        <div class="user_info_box">
          <span class="info_item">닉네임</span>
          <span class="gap"></span>
          <span class="info_item">${date} ${time}</span>
        </div>
        <div class="btn_wrapper">
        <button class="btn_reply_setting">
          <i class="fa-solid fa-ellipsis" style="color: #333333;" aria-hidden="true"></i>
        </button>
        </div>
      </div>
    </div>
    <div class="reply_content">${text}</div>
    <div class="reply_actions">
      <button class="btn_toggle_nested_reply"><i class="fa-regular fa-comment-dots"></i><span class="nested-reply-count">0</span></button>
    </div>
  `;
  return item;
}

// 댓글 아이템에 대댓글 섹션을 추가하는 함수
function addNestedReplySection(replyItem) {
  // 이미 섹션이 존재하면 추가하지 않음
  if (replyItem.querySelector('.nested-reply-section')) return;

  const nestedReplySection = document.createElement('div');
  nestedReplySection.className = 'nested-reply-section';
  nestedReplySection.innerHTML = `
    <div class="nested-reply-write-area">
      <textarea class="nested-reply-textarea" rows="1" placeholder="대댓글 달기..."></textarea>
      <button class="reply_btn nested-reply-btn">등록</button>
    </div>
    <div class="nested-reply-list"></div>
  `;
  replyItem.appendChild(nestedReplySection);

  // textarea 입력에 따라 등록 버튼 활성화/비활성화
  const textarea = nestedReplySection.querySelector('.nested-reply-textarea');
  const button = nestedReplySection.querySelector('.nested-reply-btn');

  if (textarea && button) {
    textarea.addEventListener('input', () => {
      button.classList.toggle('disabled', textarea.value.trim().length === 0);
    });
    button.classList.add('disabled'); // 초기에는 비활성화
  }
}


// 부모 댓글 아이템에 대댓글을 추가하는 함수
function addNestedReply(parentReplyItem, text) {
  if (!text) return;

  const now = new Date();
  const date = `${now.getFullYear()}.${String(now.getMonth()+1).padStart(2,'0')}.${String(now.getDate()).padStart(2,'0')}`;
  const time = now.toTimeString().slice(0,5);

  const nestedReplyList = parentReplyItem.querySelector('.nested-reply-list');
  if (!nestedReplyList) return;

  const newReply = document.createElement('div');
  newReply.className = 'reply_item nested-reply-item'; // 대댓글임을 나타내는 클래스 추가
  newReply.innerHTML = `
    <div class="reply_header" style="width:100%">
      <div class="reply_wrapper">
        <div class="user_info_box">
          <span class="info_item">닉네임</span>
          <span class="gap"></span>
          <span class="info_item">${date} ${time}</span>
        </div>
        <div class="btn_wrapper">
        <button class="btn_reply_setting">
          <i class="fa-solid fa-ellipsis" style="color: #333333;" aria-hidden="true"></i>
        </button>
        </div>
      </div>
    </div>
    <div class="reply_content">${text}</div>
    <div class="reply_actions">
      <button class="btn_toggle_nested_reply"><i class="fa-regular fa-comment-dots"></i><span class="nested-reply-count">0</span></button>
    </div>
  `;
  nestedReplyList.appendChild(newReply); // 중첩된 목록에 추가

  // 새로 생성된 대댓글에도 대댓글 섹션 추가 (재귀적 중첩 가능)
  addNestedReplySection(newReply);
  updateNestedReplyCount(parentReplyItem); // 부모 댓글의 대댓글 수 업데이트
  closeAllReplyMenus(); // 열려있는 메뉴 닫기
}


// 4) 댓글 수 배지 업데이트 (말풍선 옆 .count)
function updateCommentCount(post) {
  const replyBtn = post.querySelector('.comment_footer .btn_reply');
  if (!replyBtn) return;
  // 최상위 댓글만 카운트 (nested-reply-item 클래스가 없는 댓글)
  const cnt = post.querySelectorAll('.reply_item:not(.nested-reply-item)').length;
  let badge = replyBtn.querySelector('.count');
  if (!badge) {
    badge = document.createElement('span');
    badge.className = 'count';
    replyBtn.appendChild(badge);
  }
  badge.textContent = String(cnt);
}

// 특정 댓글 아이템의 대댓글 수를 업데이트하는 함수
function updateNestedReplyCount(replyItem) {
  const nestedReplyCountSpan = replyItem.querySelector('.nested-reply-count');
  if (nestedReplyCountSpan) {
    const nestedReplyList = replyItem.querySelector('.nested-reply-list');
    if (nestedReplyList) {
      const count = nestedReplyList.querySelectorAll('.nested-reply-item').length;
      nestedReplyCountSpan.textContent = String(count);
    } else {
      nestedReplyCountSpan.textContent = '0'; // 대댓글 리스트가 없으면 0으로 설정
    }
  }
}

// 5) 메뉴 토글 재사용 헬퍼
function toggleMenu(btn, html, cls) {
  const container = btn.parentElement;
  const existing = container.querySelector(`.${cls}`);
  if (existing) {
    existing.remove();
    return;
  }
  const menu = document.createElement('div');
  menu.className = cls;
  menu.innerHTML = html;
  container.appendChild(menu);
}

// 6) 댓글 메뉴 닫기 헬퍼
function closeAllReplyMenus() {
  document.querySelectorAll('.reply-settings-menu').forEach(m => m.remove());
}

// --- 모달 닫기 함수 추가 ---
function closeImageModal() {
  const modal = document.getElementById('image-modal');
  if (modal) modal.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('image-modal');
  const imgEl = document.getElementById('modal-img');
  const closeBtn = modal.querySelector('.image-modal-close');
  applyImageOrientation();
  // --- 이미지 방향에 따라 클래스 붙이기 ---
  document.querySelectorAll('.comment_contents img').forEach(img => {
    const applyClass = () => {
      const cls = img.naturalWidth > img.naturalHeight ? 'landscape' : 'portrait';
      img.classList.add(cls);
    };
    if (img.complete) {
      applyClass();
    } else {
      img.addEventListener('load', applyClass);
    }
  });

  let scale = 1,
    isDrag = false,
    startX = 0,
    startY = 0,
    offX = 0,
    offY = 0;

  // 1) 이미지 클릭 → 모달 열기
  document.body.addEventListener('click', e => {
    // .comment_contents 내의 <img>를 클릭했을 때
    if (e.target.matches('.comment_contents img')) {
      scale = 1;
      offX = 0;
      offY = 0;
      imgEl.src = e.target.src;
      imgEl.style.transform = 'translate(-50%, -50%) translate(0,0) scale(1)';
      modal.style.display = 'block';
    }
  });

  // 3) 닫기 버튼 클릭 → 모달 닫기
  closeBtn.addEventListener('click', closeImageModal);

  // 4) 휠로 줌 인·아웃
  modal.addEventListener('wheel', e => {
    e.preventDefault();
    scale = e.deltaY < 0 ? Math.min(scale + 0.1, 5) : Math.max(scale - 0.1, 1);
    imgEl.style.transform = `translate(-50%, -50%) translate(${offX}px,${offY}px) scale(${scale})`;
  }, {
    passive: false
  });

  // 5) 드래그로 이동
  imgEl.addEventListener('mousedown', e => {
    e.preventDefault();
    isDrag = true;
    startX = e.clientX;
    startY = e.clientY;
    imgEl.style.cursor = 'grabbing';
  });
  document.addEventListener('mousemove', e => {
    if (!isDrag) return;
    const dx = e.clientX - startX,
      dy = e.clientY - startY;
    startX = e.clientX;
    startY = e.clientY;
    offX += dx;
    offY += dy;
    imgEl.style.transform = `translate(-50%, -50%) translate(${offX}px,${offY}px) scale(${scale})`;
  });
  document.addEventListener('mouseup', () => {
    if (isDrag) {
      isDrag = false;
      imgEl.style.cursor = 'grab';
    }
  });
  imgEl.style.cursor = 'grab';
});
// ── 이미지 방향에 따라 클래스 붙이는 함수 ──
function applyImageOrientation() {
  document.querySelectorAll('.comment_contents img').forEach(img => {
    const setOri = () => {
      // 기존 inline style 제거
      img.removeAttribute('style');
      // 방향에 따라 클래스 추가
      img.classList.remove('landscape', 'portrait');
      img.classList.add(
        img.naturalWidth > img.naturalHeight ? 'landscape' : 'portrait'
      );
    };
    // 로딩 완료 여부 체크
    if (img.complete) setOri();
    else img.addEventListener('load', setOri);
  });
}

// 게시글 백엔드
async function loadPosts() {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/posts/');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const posts = await response.json(); // JSON 데이터를 파싱합니다.

    const postListContainer = document.querySelector('.post-list'); // 게시물들이 들어갈 컨테이너
    postListContainer.innerHTML = ''; // 기존 내용 지우기

    posts.forEach(post => {
      const postElement = createPostElement(post); // 아래에서 만들 함수
      postListContainer.appendChild(postElement);
    });

  } catch (error) {
    console.error('게시물을 가져오는 중 오류 발생:', error);
  }
}

function createPostElement(post) {
    const postDiv = document.createElement('div');
    postDiv.className = 'post';
    postDiv.innerHTML = `
        <div class="profile-area">
            <img src="${post.image ? post.image : 'default_profile.png'}" alt="Profile" class="profile-img">
            <span class="user-id">${post.author.username}</span>
        </div>
        <div class="post-content-area">
            <p>${post.content}</p>
            ${post.title ? `<h4>${post.title}</h4>` : ''}
            ${post.image ? `<img src="${post.image}" alt="Post Image" class="post-image">` : ''}
            <div class="post-meta">
                <span>${new Date(post.created_at).toLocaleString()}</span>
            </div>
        </div>
        <div class="comment_footer">
            <button class="btn_like"><i class="fa-solid fa-thumbs-up"></i> <span class="text">${post.likes_count}</span></button>
            <button class="btn_reply"><i class="fa-solid fa-comment"></i> <span class="count">${post.comments ? post.comments.length : 0}</span></button>
            <div class="right_area">
                <button class="btn_setting"><i class="fa-solid fa-ellipsis-vertical"></i></button>
            </div>
        </div>
        <div class="reply_area">
            <div class="reply_wrap">
                <div class="reply_write_area active">
                  <div class="comment-box">
                      <textarea class="reply_textarea" rows="1" placeholder="댓글 달기..." data-post-id="${post.id}"></textarea>
                      <button class="reply_btn" data-post-id="${post.id}"><i class="fa-solid fa-paper-plane"></i></button>
                  </div>    
                </div>
                <div class="reply_list_area">
                    <div class="reply_list">
                        ${post.comments ? post.comments.map(comment => createReplyItem(comment.content)).join('') : ''}
                    </div>
                </div>
            </div>
        </div>
    `;
    // 게시글 생성 후, 해당 게시글의 모든 댓글에 대해 대댓글 섹션 초기화 및 대댓글 수 업데이트
    postDiv.querySelectorAll('.reply_item').forEach(replyItem => {
        addNestedReplySection(replyItem);
        updateNestedReplyCount(replyItem); // 초기 대댓글 수 설정
    });
  return postDiv;
}

// 페이지 로드 시 게시물 로딩 함수 호출
document.addEventListener('DOMContentLoaded', () => {
  loadPosts();
});