from django.shortcuts import render, redirect
from . models import ReadingGroup  # 그룹 모델
from booksearch. models import Book
from django.http import JsonResponse  # 책 검색 모달창 api 관련
import requests, urllib # 책 검색 모달창 api 관련

def ajax_search(request):
    query = request.GET.get('query', '').strip()
    if not query:
        return JsonResponse({"books": []})
    headers = {
        "Authorization": "KakaoAK 5262b6fed76275833a5b8806921d6af1"  # ← 너의 REST API 키로 바꾸기!
    }
    params = {
        "query": query,
        "size": 20,
        "page": 1,
    }
    response = requests.get("https://dapi.kakao.com/v3/search/book", headers=headers, params=params)
    if response.status_code != 200:
        return JsonResponse({"error": "API 요청 실패"}, status=500)
    data = response.json()
    documents = data.get('documents', [])
    books = []
    for doc in documents:
        title = doc.get('title', '')
        authors = ", ".join(doc.get('authors', []))
        publisher = doc.get('publisher', '')
        thumbnail = doc.get('thumbnail', '')
        isbn_raw = doc.get('isbn', '')
        isbn = isbn_raw.split()[-1] if isbn_raw else ""
        # 고화질 이미지 추출
        if 'fname=' in thumbnail:
            cover = urllib.parse.unquote(thumbnail.split("fname=")[-1])
        else:
            cover = thumbnail
            books.append({
                "title": title,
                "author": authors,
                "publisher": publisher,
                "cover": cover,
                "isbn": isbn,
            })
    return JsonResponse({"books": books})


# 2. 교환독서_그룹만들기 | Share_AddGroup
def Share_AddGroup(request):
    if request.method == 'GET':
        books = Book.objects.all()  # DB에서 전체 book 가져오기
        return render(request,'shareMain/Share_AddGroup.html', {'books': books})
    
    elif request.method == 'POST' :
        # 회원정보 DB저장
        group_name = request.POST.get('group_name')
        member_count = int(request.POST.get('member_count'))
        description = request.POST.get('description','')
        book = request.POST.get('book')
        tag = request.POST.get('tag')
        is_public = int(request.POST.get('is_public'))  # 체크 안 하면 0
        password = request.POST.get('password')
        
        # 🔹 책 정보 (숨겨진 input으로부터)
        title = request.POST.get('book_title')
        author = request.POST.get('book_author')
        cover = request.POST.get('book_cover')
        isbn = request.POST.get('book_isbn')

        if not title or not author:
            return render(request, 'shareMain/Share_AddGroup.html', {
                'books': Book.objects.all(),
                'error': "책을 선택해주세요."
            })
        # 🔸 Book이 DB에 이미 있는지 확인 (isbn으로)
        book_obj = Book.objects.filter(ISBN=isbn).first()
        if not book_obj:
            # 없으면 새로 생성
            book_obj = Book.objects.create(
                title=title,
                author=author,
                cover=cover,
                ISBN=isbn,
                publisher='',  # 필요시 수정
                book_url='',    # 필요시 수정
                pub_date=None   # 필요시 수정
            )
        # 그룹 저장
        ReadingGroup.objects.create(
            group_name=group_name,
            member_count=member_count,
            description=description,
            book=book_obj,
            tag=tag,
            is_public=is_public,
            password=password,
        )
        return redirect('shareMain:Share_Main')  # 생성 후 메인으로 이동


# 1. 교환독서_메인페이지 | Share_Main
def Share_Main(request):
    groups = ReadingGroup.objects.all().order_by('-id')  # 최신순 정렬
    
    for group in groups:
        group.tags_list = group.tag.split(",")
    
    return render(request, 'shareMain/Share_Main.html', {'groups':groups})
