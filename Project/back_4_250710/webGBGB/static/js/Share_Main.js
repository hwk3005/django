// document.getElementById("group-search-input").addEventListener("input", function () {
//     const query = this.value;

//     fetch(`/shareMain/search-groups/?q=${encodeURIComponent(query)}`)
//         .then((response) => response.json())
//         .then((data) => {
//             // 🔽 그룹 리스트 영역 비우고 새로 추가
//             const resultContainer = document.getElementById("group-list");
//             resultContainer.innerHTML = "";

//             data.groups.forEach((group) => {
//                 const item = document.createElement("div");
//                 item.className = "group-item";
//                 item.innerHTML = `
//                     <h3>${group.name}</h3>
//                     <p>책 제목: ${group.book_title}</p>
//                     <p>저자: ${group.book_author}</p>
//                     <p>소개: ${group.description}</p>
//                 `;
//                 resultContainer.appendChild(item);
//             });
//         });
// });
