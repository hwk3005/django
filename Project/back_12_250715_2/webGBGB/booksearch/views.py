from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from booksearch.models import Book
from review.models import Review, ReviewLike
from reply.models import Reply
from member.models import Member
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.db.models import F, Q
from django.core.paginator import Paginator
import traceback
from django.contrib import messages
from shareMain.models import ReadingGroup
import datetime
import html


def search(request):
    review_count = Review.objects.count()

    query = request.GET.get('query', '').strip() or '파이썬'
    query_lower = query.lower()
    total_count = 0

    member_id = request.session.get('user_id')
    member = None
    bookmarks = set()
    if member_id:
        try:
            member = Member.objects.get(id=member_id)
            from bookmark.models import Bookmark
            bookmarks = set(
                Bookmark.objects.filter(member_id=member.member_id)
                .values_list('book_id', flat=True)
            )
        except Member.DoesNotExist:
            member = None

    # 1. API로 검색 결과 받아오기
    headers = {
        "Authorization": "KakaoAK 5262b6fed76275833a5b8806921d6af1"
    }
    max_apipage = 2

    for apipage in range(1, max_apipage + 1):
        params = {
            "query": query,
            "size": 50,
            "page": apipage,
        }
        response = requests.get("https://dapi.kakao.com/v3/search/book?sort=accuracy", headers=headers, params=params)
        if response.status_code != 200:
            print("❌ API 오류:", response.status_code)
            print("에러 내용:", response.text)
            break

        data = response.json()
        documents = data.get('documents', [])

        for doc in documents:
            title = html.unescape(doc.get('title', ''))
            author = html.unescape(", ".join(doc.get('authors', [])))
            publisher = html.unescape(doc.get('publisher', ''))
            thumbnail_url = doc.get('thumbnail', '')
            book_url = doc.get('url', '')

            # 고화질 이미지 추출
            if 'fname=' in thumbnail_url:
                cover = urllib.parse.unquote(thumbnail_url.split("fname=")[-1])
            else:
                cover = thumbnail_url

            pub_date_raw = doc.get('datetime', '')
            pub_date = pub_date_raw[:10] if pub_date_raw else None

            isbn_raw = doc.get('isbn', '')
            isbn = isbn_raw.split()[-1] if isbn_raw else "정보없음"

            # 2. title 또는 author에 쿼리 포함되는 경우만 DB에 저장
            if query_lower in title.lower() or query_lower in author.lower():
                if not Book.objects.filter(title=title, publisher=publisher).exists():
                    Book.objects.create(
                        book_url=book_url,
                        title=title,
                        author=author,
                        publisher=publisher,
                        cover=cover,
                        pub_date=pub_date,
                        ISBN=isbn
                    )
        if data.get('meta', {}).get('is_end'):
            break

    # 2. Book DB에서 쿼리로 contains 검색
    book_qs = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query)
    )

    total_count = book_qs.count()

    page = int(request.GET.get('page', 1))
    per_page = 20  # 한 페이지에 20개
    block_size = 5 # 한 블록에 5페이지

    paginator = Paginator(book_qs, per_page)
    page_obj = paginator.get_page(page)
    total_pages = paginator.num_pages

    # 블록 계산
    block_num = (page - 1) // block_size
    block_start = block_num * block_size + 1
    block_end = min(block_start + block_size - 1, total_pages)
    page_range = range(block_start, block_end + 1)

    has_prev_block = block_start > 1
    has_next_block = block_end < total_pages
    prev_block_page = block_start - 1
    next_block_page = block_end + 1
    
    print("page:", page)
    print("total_pages:", total_pages)
    print("block_start:", block_start)
    print("block_end:", block_end)
    print("has_prev_block:", has_prev_block)
    print("has_next_block:", has_next_block)

    context = {
        'books': page_obj,
        'bookmarks': bookmarks,
        'query': query,
        'page_obj': page_obj,
        'paginator': paginator,
        'page_range': page_range,
        'block_start': block_start,
        'block_end': block_end,
        'total_pages': total_pages,
        'total_count': f"{total_count:,}",
        'has_prev_block': has_prev_block,
        'has_next_block': has_next_block,
        'prev_block_page': prev_block_page,
        'next_block_page': next_block_page,
        'member': member,  # 로그인 여부를 템플릿에서 확인 가능
        'review_count':review_count,
    }

    return render(request, 'booksearch/booksearch.html', context)

def detail(request, book_id):
    print("넘어온 book_id : ", book_id)
    review_count = Review.objects.count()


    member_id = request.session.get('user_id')
    member = None

    bookmarks = set()
    if member_id:
        try:
            member = Member.objects.get(id=member_id)
            from bookmark.models import Bookmark
            bookmarks = set(
                Bookmark.objects.filter(member_id=member.member_id)
                .values_list('book_id', flat=True)
            )
        except Member.DoesNotExist:
            member = None

    try:
        book = Book.objects.get(book_id=book_id)
    except Book.DoesNotExist:
        return render(request, 'booksearch/404.html', status=404)
    
    reviews_qs = Review.objects.filter(book_id=book).prefetch_related('images').order_by('-created_at')
    for r in reviews_qs:
        r.rating_percent = r.rating * 20
        r.reply_list = Reply.objects.filter(review_id=r).order_by('created_at')
        
    user_liked_review_ids = set()
    if member:
        user_liked_review_ids = set(
            ReviewLike.objects.filter(member_id=member).values_list('review_id', flat=True)
        )


    total_count = reviews_qs.count()
    
    reading_group = ReadingGroup.objects.filter(book_id=book_id).order_by('-created_at')[:5]
    if reading_group is None:
        # 원하는 처리 (예: None 처리)
        pass
    else:
        # 객체가 있을 때 처리
        pass
    
    print("조회수 증가 book_id:", book.book_id)
    updated = Book.objects.filter(book_id=book.book_id).update(views=F('views') + 1)
    print("조회수 증가 update 결과:", updated)    
    book.refresh_from_db()

    page_str = request.GET.get('page', '1')
    try:
        page = int(page_str)
    except (TypeError, ValueError):
        page = 1
    per_page = 5  # 한 페이지에 5개
    block_size = 5 # 한 블록에 5페이지

    paginator = Paginator(reviews_qs, per_page)
    page_obj = paginator.get_page(page)
    total_pages = paginator.num_pages

    # 블록 계산
    block_num = (page - 1) // block_size
    block_start = block_num * block_size + 1
    block_end = min(block_start + block_size - 1, total_pages)
    page_range = range(block_start, block_end + 1)

    has_prev_block = block_start > 1
    has_next_block = block_end < total_pages
    prev_block_page = block_start - 1
    next_block_page = block_end + 1
    
    print("page:", page)
    print("total_pages:", total_pages)
    print("block_start:", block_start)
    print("block_end:", block_end)
    print("has_prev_block:", has_prev_block)
    print("has_next_block:", has_next_block)

    # 북마크 여부 확인
    is_bookmarked = False
    if member:
        from bookmark.models import Bookmark
        is_bookmarked = Bookmark.objects.filter(book_id=book, member_id=member.member_id).exists()

    # 이미 DB에 값이 있으면 크롤링 생략
    if (not book.page or book.page == 0) or (not book.size or book.size.strip() == ""):
        page_rv = ''
        size_rv = ''
        if hasattr(book, 'book_url') and book.book_url:
            try:
                options = Options()
                options.add_argument("--headless")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("start-maximized")
                options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)

                browser = webdriver.Chrome(options=options)
                url = book.book_url
                browser.get(url)
                soup = BeautifulSoup(browser.page_source, "lxml")
                browser.quit()

                page_rv, size_rv = "정보없음","정보없음"

                data = soup.find("div", class_="wrap_cont")
                if not data:
                    # 값이 없으면 바로 종료
                    return

                for dl in data.find_all("dl", class_="dl_comm dl_row"):
                    dt = dl.find("dt", class_="tit_base")
                    if dt and dt.get_text(strip=True) == "페이지수":
                        dd = dl.find("dd", class_="cont")
                        if dd:
                            # 페이지수 추출
                            page_rv = dd.get_text(" ", strip=True).split('|')[0].strip()
                            # 판형(사이즈) 추출
                            size_span = dd.find("span", class_="txt_tag")
                            size_rv = size_span.next_sibling.strip() if size_span and size_span.next_sibling else "정보없음"
                        break  # 찾았으면 반복 종료

            except Exception as e:
                print("Selenium 크롤링 오류:", e)
                traceback.print_exc()
            
            # Book 모델에 저장
            updated = False
            if page_rv:
                try:
                    book.page = page_rv
                    updated = True
                except ValueError:
                    pass
            if size_rv and book.size != size_rv:
                book.size = size_rv
                updated = True
            if updated:
                book.save()
        # end if hasattr(book, 'book_url') and book.book_url
        
    average = book.rating / book.review_count if book.review_count > 0 else 0
    average_percent = average * 20


    # context 및 렌더링
    context = {
        'book': book,
        'reviews': page_obj,
        'bookmarks': bookmarks,
        'total_count': f"{total_count:,}",
        'average':average,
        'average_percent':average_percent,
        'page_obj': page_obj,
        'paginator': paginator,
        'page_range': page_range,
        'block_start': block_start,
        'block_end': block_end,
        'total_pages': total_pages,
        'has_prev_block': has_prev_block,
        'has_next_block': has_next_block,
        'prev_block_page': prev_block_page,
        'next_block_page': next_block_page,
        'member': member,
        'user_liked_review_ids': user_liked_review_ids,
        'reading_group':reading_group,
        'review_count':review_count,
    }
    response = render(request, 'booksearch/bookdetail.html', context)
    return response
