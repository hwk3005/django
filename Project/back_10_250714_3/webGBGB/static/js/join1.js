document.addEventListener("DOMContentLoaded", function() {
  const allAgreeCheckbox = document.querySelector(".chchch"); // "모두 동의" 체크박스
  const individualAgreeCheckboxes = document.querySelectorAll(".saveAgree"); // 개별 약관 동의 체크박스들
  const agreeForm = document.getElementById("agreeFrm"); // 폼

  // 폼 제출 시 모든 약관 동의 확인
  agreeForm.addEventListener("submit", function(event) {
    const allChecked = Array.from(individualAgreeCheckboxes).every(checkbox => checkbox.checked);

    if (!allChecked) {
      event.preventDefault(); // 제출 중단
      alert("모든 약관에 동의해야 가입할 수 있습니다.");
    }
  });

  // "모두 동의" 체크박스 변경 시 개별 약관 동의 체크박스 상태 변경
  allAgreeCheckbox.addEventListener("change", function() {
    individualAgreeCheckboxes.forEach(checkbox => {
      checkbox.checked = this.checked;
    });
  });

  // 개별 약관 동의 체크박스 변경 시 "모두 동의" 체크박스 상태 변경
  individualAgreeCheckboxes.forEach(checkbox => {
    checkbox.addEventListener("change", function() {
      const allIndividualChecked = Array.from(individualAgreeCheckboxes).every(cb => cb.checked);
      allAgreeCheckbox.checked = allIndividualChecked;
    });
  });
});