from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from review.models import Review

def chajax(request):
    if request.method == "POST":
        book_id = request.POST.get('bookId')
        TAGS = ["집중돼요", "도움돼요", "쉬웠어요", "최고예요", "추천해요"]

        # 태그별 개수 집계
        tag_counts_qs = (
            Review.objects.filter(book_id=book_id, tag__in=TAGS)
            .values('tag')
            .annotate(count=Count('tag'))
        )

        # 기본값 0으로 딕셔너리 생성
        tag_counts = {tag: 0 for tag in TAGS}
        for item in tag_counts_qs:
            tag_counts[item['tag']] = item['count']

        return JsonResponse({'tag_counts': tag_counts})
    return JsonResponse({'error': 'Invalid request'}, status=400)
