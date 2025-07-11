from django.shortcuts import render, redirect
from .models import ReadingGroup # shareMain 앱의 모델 불러오기
from .forms import ReadingGroupForm  # ReadingGroupForm
from booksearch.models import Book  # book 앱의 모델 불러오기
from member.models import Member  # member 앱의 모델 불러오기

from django.http import JsonResponse  # 책 검색 모달창 api 관련
import requests, urllib, urllib.parse # 책 검색 모달창 api 관련
from django.db.models import Q  # 메인페이지_그룹 검색 관련
from django.contrib import messages  # Share_AddGroup 로그인 관련
from django.core.paginator import Paginator  # 페이지네이터 관련


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


# 2-3. 교환독서_그룹만들기 | paginator
def get_group_paginator(request):
    page = int(request.GET.get('page', 1))
    query = request.GET.get('q', '').strip()
    if query:
        groups_qs = ReadingGroup.objects.filter(
            Q(group_name__icontains=query) |
            Q(book__title__icontains=query) |
            Q(book__author__icontains=query) |
            Q(tag__icontains=query)
        ).distinct().order_by('-id')
    else:
        groups_qs = ReadingGroup.objects.all().order_by('-id')
    paginator = Paginator(groups_qs, 10)
    groups = paginator.get_page(page)
    for g in groups:
        g.tag_list = g.tag.split(",") if g.tag else []
    return groups, query


# 2-2. 교환독서_그룹만들기 | api 관련
def ajax_search(request):
    query = request.GET.get('query', '').strip()
    page = int(request.GET.get('page', 1))  # ← 페이지 파라미터 받기 (기본값 1)

    if not query:
        return JsonResponse({"books": [], "pagination": {}})

    headers = {
        "Authorization": "KakaoAK 5262b6fed76275833a5b8806921d6af1"  # ← 너의 REST API 키로 바꾸기!
    }
    params = {
        "query": query,
        "size": 20,
        "page": 1,   # Kakao API는 1~50까지 지원
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

        # ISBN-13(13자리)로만 저장
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
        # 이 줄 들여쓰기 주의 (밖으로 빼야 함)
        books.append({
            "title": title,
            "author": authors,
            "publisher": publisher,
            "cover": cover,
            "isbn": isbn,
        })

    # 페이지네이터 적용 (1페이지에 10권씩)
    paginator = Paginator(books, 10)
    page_obj = paginator.get_page(page)
    books_page = list(page_obj.object_list)

    pagination = {
        "has_previous": page_obj.has_previous(),
        "has_next": page_obj.has_next(),
        "num_pages": paginator.num_pages,
        "current_page": page_obj.number,
        "page_range": list(paginator.page_range),
        "previous_page_number": page_obj.previous_page_number() if page_obj.has_previous() else None,
        "next_page_number": page_obj.next_page_number() if page_obj.has_next() else None,
    }

    return JsonResponse({
        "books": books_page,
        "pagination": pagination,
    })


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
    # 검색 파라미터 (q로 통일)
    query = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))

    # 검색/전체 그룹 쿼리셋
    if query:
        groups = ReadingGroup.objects.filter(
            Q(group_name__icontains=query) |
            Q(book__title__icontains=query) |
            Q(book__author__icontains=query) |
            Q(tag__icontains=query)
        ).distinct().order_by('-id')
    else:
        groups = ReadingGroup.objects.all().order_by('-id')

    # 페이지네이터 적용
    paginator = Paginator(groups, 10)  # 10개씩
    groups = paginator.get_page(page)  # groups는 Page 객체

    # 각 그룹별로 tag_list 속성 추가
    for group in groups:
        group.tag_list = group.tag.split(",") if group.tag else []

    # 로그인 시 참여 그룹
    join_groups = []
    member_id = request.session.get('member_id')
    if member_id:
        try:
            member = Member.objects.get(member_id=member_id)
            join_groups = ReadingGroup.objects.filter(
                Q(admin=member) | Q(member=member)
            ).distinct().order_by('-id')[:8]
        except Member.DoesNotExist:
            pass

    context = {
        'groups': groups,  # paginator Page 객체
        'join_groups': join_groups,
        'member':member, # member추가
        'query': query,    # 검색어도 같이 넘김 (페이지네이터에서 필요)
    }
    return render(request, 'shareMain/Share_Main.html', context)
