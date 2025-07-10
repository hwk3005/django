from django.shortcuts import render, redirect
from .models import ReadingGroup
from booksearch.models import Book
from .forms import ReadingGroupForm

from django.http import JsonResponse  # 책 검색 모달창 api 관련
import requests, urllib # 책 검색 모달창 api 관련
from django.db.models import Q  # 메인페이지_그룹 검색 관련
from member.models import Member  # member 앱의 모델 불러오기
from django.contrib import messages  # Share_AddGroup 로그인 관련

# 3. 참여 중인 그룹 수 제한
def join_group(request, group_id):
    member_id = request.session.get('member_id')
    if not member_id:
        return redirect('member:login')
    member = Member.objects.get(member_id=member_id)
    group = ReadingGroup.objects.get(id=group_id)

    # 참여한 그룹 수 체크
    joined_count = ReadingGroup.objects.filter(
        Q(admin=member) | Q(member=member)
        ).distinct().count()
    if joined_count >= 8:
        messages.warning(request, '최대 8개의 그룹만 참여할 수 있습니다.')
        return redirect('shareMain:Share_Main')

    # 중복 가입 방지
    if group.member.filter(member_id=member_id).exists():
        messages.info(request, '이미 참여 중인 그룹입니다.')
        return redirect('shareMain:Share_Main')

    group.member.add(member)
    messages.success(request, '그룹에 가입되었습니다!')
    return redirect('shareMain:Share_Main')


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

        # ISBN-13(13자리)로만 저장하는 게 안전
        isbn13 = ''
        for num in isbn_raw.split():
            if len(num) == 13:
                isbn13 = num
                break
        isbn = isbn13 or (isbn_raw.split()[-1] if isbn_raw else "")
        
        # isbn_raw 전체를 로그로 출력!
        print(f"[Kakao API] {title} | isbn_raw: {isbn_raw}")
        
        
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
    # 로그인한 유저 정보 가져오기
    member_id = request.session.get('member_id')
    if not member_id:
        messages.warning(request, '로그인이 필요합니다.')
        return redirect('member:login')  # 로그인 페이지로
    try:
        member = Member.objects.get(member_id=member_id)
    except Member.DoesNotExist:
        return redirect('member:login')  # 세션에 이상 있으면 로그인 요구
    
    if request.method == 'POST':
        form = ReadingGroupForm(request.POST)
        if form.is_valid():
            # 책 정보 꺼내기
            isbn = form.cleaned_data['book_isbn']
            title = form.cleaned_data['book_title']
            author = form.cleaned_data['book_author']
            cover = form.cleaned_data['book_cover']
            publisher = form.cleaned_data.get('book_publisher', '')

            if not isbn or not title:
                return render(request, 'shareMain/Share_AddGroup.html', {
                    'form': form,
                    'error': '책을 선택해주세요.',
                })
            # Book DB 저장 or get
            book_obj, created = Book.objects.get_or_create(
                ISBN=isbn,
                title=title,
                author=author,
                defaults={
                    'title': title,
                    'author': author,
                    'cover': cover,
                    'publisher': publisher,
                }
            )
            # 1. 참여 중인 그룹 수 확인
            joined_count = ReadingGroup.objects.filter(
                Q(admin=member) | Q(member=member)
            ).distinct().count()

            if joined_count >= 8:
                messages.warning(request, '최대 8개의 그룹만 참여할 수 있습니다. 그룹을 더 만들 수 없습니다.')
                return redirect('shareMain:Share_Main')
            
            # 2. 그룹 생성
            group = form.save(commit=False)
            group.book = book_obj
            group.admin = member  # 방장 지정
            group.save()

            # 3. 자신도 멤버로 추가
            group.member.add(member)

            return redirect('shareMain:Share_Main')
        else:
            print("폼 오류:", form.errors)
            return render(request, 'shareMain/Share_AddGroup.html', {'form': form})
    else:
        form = ReadingGroupForm()
        return render(request, 'shareMain/Share_AddGroup.html', {'form': form})


# 1. 교환독서_메인페이지 | Share_Main
def Share_Main(request):
    # 검색창 - 검색기능 부분
    groups = ReadingGroup.objects.all().order_by('-id')  # 최신순 정렬
    query = request.GET.get('q', '')
    if query:
        groups = ReadingGroup.objects.filter(
            Q(group_name__icontains=query) |
            Q(book__title__icontains=query) |
            Q(book__author__icontains=query) |
            Q(tag__icontains=query)
        ).distinct().order_by('-id')  # 검색 결과도 최신순 정렬
    else:
        groups = ReadingGroup.objects.all().order_by('-id')  # 전체 그룹 최신순 정렬
        
    # 로그인 시 참여 중인 그룹 가져오기
    join_groups = []
    member_id = request.session.get('member_id')

    if member_id:
        print("세션에 저장된 member_id:", member_id)  # ← 디버그용
        try:
            member = Member.objects.get(member_id=member_id)
            join_groups = ReadingGroup.objects.filter(
                Q(admin=member) | Q(member=member)
            ).distinct().order_by('-id')[:8]  # 최신순으로 8개만
            print("참여 그룹 수:", join_groups.count())
        except Member.DoesNotExist:
            print("Member 객체 못 찾음")

    context = {
        'groups':groups,
        'join_groups': join_groups,  # 로그인한 유저의 참여 그룹
    }
    return render(request, 'shareMain/Share_Main.html', context)


