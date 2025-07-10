from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from booksearch.models import Book
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.db.models import Q
import traceback


def search(request):
    query = request.GET.get('query', '').strip() or '파이썬'
    query_lower = query.lower()
    books = []
    total_count = 0

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
        response = requests.get("https://dapi.kakao.com/v3/search/book", headers=headers, params=params)
        if response.status_code != 200:
            print("❌ API 오류:", response.status_code)
            print("에러 내용:", response.text)
            break

        data = response.json()
        documents = data.get('documents', [])

        for doc in documents:
            title = doc.get('title', '')
            author = ", ".join(doc.get('authors', []))
            publisher = doc.get('publisher', '')
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
            isbn = isbn_raw.split()[-1] if isbn_raw else None

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
        apipage += 1

    # 2. Book DB에서 쿼리로 contains 검색
    book_qs = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query)
    )

    total_count = book_qs.count()

    page = int(request.GET.get('page', 1))
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    page_books = book_qs[start:end]

    total_pages = (total_count + per_page - 1) // per_page

    block_size = 5
    block_num = (page - 1) // block_size
    block_start = block_num * block_size + 1
    block_end = min(block_start + block_size - 1, total_pages)

    page_range = range(block_start, block_end + 1)

    context = {
        'books': page_books,
        'bookmarks': bookmarks,
        'query': query,
        'page_range': page_range,
        'block_start': block_start,
        'block_end': block_end,
        'has_prev_block': block_start > 1,
        'has_next_block': block_end < total_pages,
        'prev_block_page': block_start - 1,
        'next_block_page': block_end + 1,
        'total_count': f"{total_count:,}",
    }

    return render(request, 'booksearch/booksearch.html', context)

def detail(request, book_id):
    print("넘어온 book_id : ", book_id)
    try:
        book = Book.objects.get(book_id=book_id)
    except Book.DoesNotExist:
        return render(request, 'booksearch/404.html', status=404)
    
    reviews = Review.objects.filter(book_id=book).prefetch_related('images').order_by('-created_at')
    for r in reviews:
        r.rating_percent = r.rating * 20
        r.reply_list = Reply.objects.filter(review_id=r).order_by('created_at')
        
    total_count = reviews.count()


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

                page_rv, size_rv = None, None

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
                            size_rv = size_span.next_sibling.strip() if size_span and size_span.next_sibling else None
                        break  # 찾았으면 반복 종료

            except Exception as e:
                print("Selenium 크롤링 오류:", e)
                traceback.print_exc()
            
            # Book 모델에 저장
            updated = False
            if page_rv:
                try:
                    book.page = int(page_rv)
                    updated = True
                except ValueError:
                    pass
            if size_rv and book.size != size_rv:
                book.size = size_rv
                updated = True
            if updated:
                book.save()
        # end if hasattr(book, 'book_url') and book.book_url

    # context 및 렌더링
    context = {
        'book': book,
    }
    return render(request, 'booksearch/bookdetail.html', context)
