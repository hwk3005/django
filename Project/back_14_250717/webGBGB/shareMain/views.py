from django.shortcuts import render, redirect
from .models import ReadingGroup # shareMain 앱의 모델 불러오기
from .forms import ReadingGroupForm  # ReadingGroupForm
from booksearch.models import Book  # book 앱의 모델 불러오기
from member.models import Member  # member 앱의 모델 불러오기
from review.models import Review

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
        "Authorization": "KakaoAK 5262b6fed76275833a5b8806921d6af1"  # ← 카카오 REST API 키
    }
    params = {
        "query": query,
        "size": 10,
        "page": page,   # Kakao API는 1~50까지 지원
    }
    response = requests.get("https://dapi.kakao.com/v3/search/book", headers=headers, params=params)
    if response.status_code != 200:
        return JsonResponse({"error": "API 요청 실패"}, status=500)
    data = response.json()
    documents = data.get('documents', [])
    meta = data.get('meta', {})
    books = []

    for doc in documents:
        title = doc.get('title', '')  # 책 제목
        authors = ", ".join(doc.get('authors', []))  # 저자
        publisher = doc.get('publisher', '')  # 출판사
        thumbnail = doc.get('thumbnail', '')  # 미리보기 이미지
        isbn_raw = doc.get('isbn', '')  # isbn
        contents = doc.get('contents', '')  # 책 소개글

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
            "contents":contents,
        })

    # 페이지네이터 적용 (Kakao meta에서 전체 결과 수, 마지막 페이지 여부 등 제공)
    total_count = meta.get('total_count', 0)
    is_end = meta.get('is_end', False)
    num_pages = (total_count // 10) + (1 if total_count % 10 else 0)
    # Kakao는 최대 50페이지(500권)까지만 지원 => 100권까지만 지원으로 변경

    pagination = {
        "has_previous": page > 1,
        "has_next": not is_end and page < num_pages,
        "num_pages": num_pages if num_pages <= 10 else 10,
        "current_page": page,
        "page_range": list(range(1, min(num_pages, 10) + 1)),
        "previous_page_number": page - 1 if page > 1 else None,
        "next_page_number": page + 1 if not is_end and page < num_pages else None,
    }

    return JsonResponse({
        "books": books,
        "pagination": pagination,
    })


# 2. 교환독서_그룹만들기 | Share_AddGroup
def Share_AddGroup(request):
    # footer 리뷰 개수 넘기기
    review_count = Review.objects.count()
    # 사용자 유효성 검사 (로그인한 유저 정보 가져오기)
    member_id = request.session.get('member_id')
    if not member_id:
        messages.warning(request, '로그인이 필요합니다.')
        return redirect('member:login')  # 로그인 페이지로
    try:
        member = Member.objects.get(member_id=member_id)
    except Member.DoesNotExist:
        return redirect('member:login')  # 세션에 이상 있으면 로그인 요구
    
    if request.method == 'POST':
        form = ReadingGroupForm(request.POST)  # 폼 제출 처리(POST요청)
        if form.is_valid():
            # 책 정보 꺼내기
            isbn = form.cleaned_data['book_isbn']
            title = form.cleaned_data['book_title']
            author = form.cleaned_data['book_author']
            cover = form.cleaned_data['book_cover']
            publisher = form.cleaned_data.get('book_publisher', '')

            if not isbn or not title:  # 책 선택 안 했을 경우 (책 제목, isbn 누락)
                return render(request, 'shareMain/Share_AddGroup.html', {
                    'form': form,
                    'error': '책을 선택해주세요.',
                })
            # 책 정보 처리 (Book 모델과 연결) Book DB 저장 or get
            book_obj, created = Book.objects.get_or_create(
                ISBN=isbn,
                title=title,
                defaults={
                    'title': title,
                    'author': author,
                    'cover': cover,
                    'publisher': publisher,
                }
            )
            # 1. 참여 중인 그룹 수 제한 체크
            joined_count = ReadingGroup.objects.filter(
                Q(admin=member) | Q(member=member)
            ).distinct().count()

            # 최대 8개 제한
            if joined_count >= 8:
                messages.warning(request, '최대 8개의 그룹만 참여할 수 있습니다. 그룹을 더 만들 수 없습니다.')
                return redirect('shareMain:Share_Main')
            # 2. 그룹 생성
            group = form.save(commit=False) # DB에 아직 저장x
            group.book = book_obj # 책 할당
            group.admin = member  # 방장 지정
            group.save()          # 이제 DB에 저장
            # 3. 자신도 멤버로 추가
            group.member.add(member)  # 자신도 참여 멤버로 등록

            return redirect('shareMain:Share_Main')  # 완료 -> 메인페이지 리다이렉트
        else:
            print("폼 오류:", form.errors)  # 폼 오류 있을 경우: cmd창에 print
            return render(request, 'shareMain/Share_AddGroup.html', {'form': form, 'review_count': review_count,})
    else:
        form = ReadingGroupForm()
        return render(request, 'shareMain/Share_AddGroup.html', {'form': form, 'review_count': review_count,} )


# 1. 교환독서_메인페이지 | Share_Main
def Share_Main(request):
    # footer 리뷰 개수 넘기기
    review_count = Review.objects.count()
    # 검색 파라미터 (q로 통일)
    query = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    member = None  # 기본값으로 선언

    # 검색/전체 그룹 쿼리셋
    if query:
        groups = ReadingGroup.objects.filter(
            Q(book__title__icontains=query) |
            Q(book__author__icontains=query) |
            Q(group_name__icontains=query) |
            Q(admin__name__icontains=query) |
            Q(tag__icontains=query)
        ).distinct().order_by('-id')
    else:
        groups = ReadingGroup.objects.all().order_by('-id')

    # 그룹 개수
    total_group_count = groups.count()

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
        'total_group_count': total_group_count,  # 총 그룹개수
        'review_count':review_count,
    }
    return render(request, 'shareMain/Share_Main.html', context)
