from django.shortcuts import render
from booksearch.models import Book
from shareMain.models import ReadingGroup
from home.models import Mainbanner

from django.shortcuts import render
from booksearch.models import Book
from shareMain.models import ReadingGroup
from home.models import Mainbanner
from review.models import Review

def index(request):
    
    review_count = Review.objects.count()
    
    # 1. 빈 데이터 템플릿 정의
    empty_book_data = {
        'title': '',
        'cover': '/static/images/Illustration28.png',
        'review_count': 0,
        'bookmark_count': 0,
        'views': 0,
        'book_id': None,
        'is_empty': True
    }
    
    empty_group_data = {
        'group_name': '',
        'book': {
            'cover': '/static/images/Illustration28.png'
        },
        'id': None,
        'is_empty': True
    }
    
    def fill_to_count(queryset, empty_data, count):
        """리스트를 지정된 개수로 채우는 헬퍼 함수"""
        items = list(queryset)
        empty_count = count - len(items)
        for i in range(empty_count):
            items.append(empty_data)
        return items
    
    # 2. 독서 그룹 데이터 (8개로 채우기)
    try:
        group_queryset = ReadingGroup.objects.all().order_by('-created_at')[:8]
        pop_group = fill_to_count(group_queryset, empty_group_data, 8)
    except:
        pop_group = [empty_group_data for _ in range(8)]
    
    # 3. 리뷰 Top5
    try:
        review_queryset = Book.objects.exclude(review_count=0).order_by('-review_count')[:5]
        review_top5 = fill_to_count(review_queryset, empty_book_data, 5)
    except:
        review_top5 = [empty_book_data for _ in range(5)]
    
    # 4. 북마크 Top5
    try:
        bookmark_queryset = Book.objects.exclude(bookmark_count=0).order_by('-bookmark_count')[:5]
        bookmark_top5 = fill_to_count(bookmark_queryset, empty_book_data, 5)
    except:
        bookmark_top5 = [empty_book_data for _ in range(5)]
    
    # 5. 조회수 Top5
    try:
        views_queryset = Book.objects.exclude(views=0).order_by('-views')[:5]
        views_top5 = fill_to_count(views_queryset, empty_book_data, 5)
    except:
        views_top5 = [empty_book_data for _ in range(5)]
    
    # 6. 메인 배너
    try:
        mainBanner = Mainbanner.objects.all().order_by('primary')
    except:
        mainBanner = []
    
    context = {
        'sharegroup': pop_group,
        'review': review_top5,
        'bookmark': bookmark_top5,
        'views': views_top5,
        'mainBanner': mainBanner,
        'review_count': review_count
    }
    
    return render(request, 'index.html', context)