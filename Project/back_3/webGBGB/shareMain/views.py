from django.shortcuts import render, redirect
from .models import ReadingGroup
from booksearch.models import Book
from .forms import ReadingGroupForm

from django.http import JsonResponse  # 책 검색 모달창 api 관련
import requests, urllib # 책 검색 모달창 api 관련

# 2-2. 교환독서_그룹만들기 | api 관련
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
        # ✅ 이 줄 들여쓰기 주의 (밖으로 빼야 함)
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
    if request.method == 'POST':
        form = ReadingGroupForm(request.POST)
        if form.is_valid():
            # ✅ 책 정보 꺼내기
            isbn = form.cleaned_data['book_isbn']
            title = form.cleaned_data['book_title']
            author = form.cleaned_data['book_author']
            cover = form.cleaned_data['book_cover']

            if not isbn or not title:
                return render(request, 'shareMain/Share_AddGroup.html', {
                    'form': form,
                    'error': '책을 선택해주세요.',
                })
            # ✅ Book DB 저장 or get
            book_obj, created = Book.objects.get_or_create(
                ISBN=isbn,
                defaults={
                    'title': title,
                    'author': author,
                    'cover': cover,
                    'publisher': '',  # 필요시 추후 반영
                    'book_url': '',
                    'pub_date': '',
                }
            )
            group = form.save(commit=False)
            group.book = book_obj
            group.save()
            return redirect('shareMain:Share_Main')
        else:
            print("폼 오류:", form.errors)  # 👈 이거!
            return render(request, 'shareMain/Share_AddGroup.html', {'form': form})
    else:
        form = ReadingGroupForm()
        return render(request, 'shareMain/Share_AddGroup.html', {'form': form})


# 1. 교환독서_메인페이지 | Share_Main
def Share_Main(request):
    groups = ReadingGroup.objects.all().order_by('-id')  # 최신순 정렬
    
    return render(request, 'shareMain/Share_Main.html', {'groups':groups})
