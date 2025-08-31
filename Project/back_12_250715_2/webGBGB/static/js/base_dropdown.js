function toggleDropdown(event) {
    event.preventDefault();
    const dropdown = document.getElementById('dropdownMenu');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

// 드롭다운 바깥 클릭 시 닫기
document.addEventListener('click', function(event) {
    if (!event.target.closest('.user-dropdown')) {
        document.getElementById('dropdownMenu').style.display = 'none';
    }
});

