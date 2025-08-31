document.addEventListener('DOMContentLoaded', function () {
  const fileList = document.querySelector('.file_list');
  const hiddenFileContainer = document.getElementById('hiddenFileInputs');
  const MAX_FILES = 3;

  let attachedFiles = [];
  let currentFileIndex = 0;



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

  // 실제 파일을 hidden input으로 추가
  function addHiddenFileInput(file) {
    const input = document.createElement('input');
    input.type = 'file';
    input.style.display = 'none';
    input.name = `uploaded_file_${currentFileIndex++}`;
    
    // File 객체를 input에 할당
    const dt = new DataTransfer();
    dt.items.add(file);
    input.files = dt.files;
    
    hiddenFileContainer.appendChild(input);
    return input;
  }

  // 파일 제거시 해당 hidden input도 제거
  function removeHiddenFileInput(file) {
    const inputs = hiddenFileContainer.querySelectorAll('input[type="file"]');
    inputs.forEach(input => {
      if (input.files.length > 0 && input.files[0] === file) {
        hiddenFileContainer.removeChild(input);
      }
    });
  }


  function createBtnBox(attached = false, imgSrc = '') {
    const id = generateId();

    const li = document.createElement('li');
    li.classList.add('list_item');
    li.innerHTML = `
      <span class="file_item ${attached ? 'attached' : ''}">
        <span class="btn_box">
          <input id="${id}" type="file" accept="image/*" />
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

        const fileData = {
          file: file,
          url: imgUrl
        };
        attachedFiles.push(fileData);
        addHiddenFileInput(file);

        // 파일 객체를 li 요소에 저장
        li.fileData = fileData;

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
        input.value = '';
      };

      reader.readAsDataURL(file);
    });

    removeBtn.addEventListener('click', () => {
        if (li.fileData) {
        const fileIndex = attachedFiles.indexOf(li.fileData);
        if (fileIndex !== -1) {
          const removedFileData = attachedFiles[fileIndex];
          attachedFiles.splice(fileIndex, 1);
          removeHiddenFileInput(removedFileData.file);
        }
      }

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

});

