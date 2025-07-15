from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from member.models import Member
from booksearch.models import Book
from bookmark.models import Bookmark
import json

@csrf_exempt  # 실제 서비스에서는 csrf_exempt 대신 CSRF 처리 권장!
@require_POST
def bookmark_create(request):
    # 1. 로그인 체크
    member_id = request.session.get('user_id')
    try:
        member = Member.objects.get(id=member_id)
    except Member.DoesNotExist:
        return JsonResponse({'error': '회원 정보가 없습니다.'}, status=404)

    # 2. JSON 데이터 파싱
    try:
        data = json.loads(request.body)
        book_id = data.get('book_id')
    except Exception:
        return JsonResponse({'error': '잘못된 요청 데이터입니다.'}, status=400)

    # 3. Book 객체 가져오기
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return JsonResponse({'error': '책 정보가 없습니다.'}, status=404)

    # 4. 북마크 토글 (있으면 삭제, 없으면 생성)
    bookmark, created = Bookmark.objects.get_or_create(member_id=member, book_id=book)
    if not created:
        bookmark.delete()
        book.bookmark_count = max(0, book.bookmark_count - 1)  # 북마크 수 -1
        book.save()
        bookmarked = False
    else:
        book.bookmark_count += 1  # 북마크 수 +1
        book.save()
        bookmarked = True

    # 5. 결과를 JSON으로 반환
    return JsonResponse({'bookmarked': bookmarked})