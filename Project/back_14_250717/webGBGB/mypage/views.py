from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import F,Q
from review.models import Review
from member.models import Member
from bookmark.models import Bookmark
from shareMain.models import ReadingGroup
from django.views.decorators.csrf import csrf_exempt

## list : 현재 페이지의 리뷰 목록
#list.paginator.num_pages : 전체 페이지 수
# list.has_previous / list.previous_page_number
# list.has_next / list.next_page_number
# page : 현재 페이지 번호

## 리뷰,멤버만 있으면 가능
def review(request):
    review_count = Review.objects.count()
    user_id = request.session.get('user_id')  # 로그인된 유저의 ID

    if not user_id:
        return redirect(f'/member/login/?next={request.path}')  # 로그인 안 되어있으면 로그인 페이지로

    try:
        member = Member.objects.get(id=user_id)  # 문자열 ID 기준으로 조회
        my_review_count = Review.objects.filter(member_id=member).count()
        my_bookmark_count = Bookmark.objects.filter(member_id=member).count()
        my_group_count = ReadingGroup.objects.filter(member=member).count()
        
    except Member.DoesNotExist:
        return redirect(f'/member/login/?next={request.path}')  # 세션은 있는데 유저가 없을 경우도 예외 처리

    page = request.GET.get('page', 1)
    qs = Review.objects.filter(member_id=member).order_by('-created_at')  # member_id는 FK니까 객체로 필터
    for r in qs:
                r.rating_percent = r.rating * 20
    paginator = Paginator(qs, 5)
    paginated_reviews = paginator.get_page(page)

    context = {
        'reviews': paginated_reviews,
        'page': int(page),
        'my_review_count': my_review_count,
        'my_bookmark_count': my_bookmark_count,
        "my_group_count": my_group_count,
        "user_id":user_id,
        'review_count':review_count,
    }

    return render(request, 'mypage/review.html', context)


def Bmark(request):
    review_count = Review.objects.count()
    user_id = request.session.get('user_id')  # 로그인된 유저의 ID

    if not user_id:
        return redirect(f'/member/login/?next={request.path}')  # 로그인 안 되어있으면 로그인 페이지로

    try:
        member = Member.objects.get(id=user_id)  # 문자열 ID 기준으로 조회
        my_review_count = Review.objects.filter(member_id=member).count()
        my_bookmark_count = Bookmark.objects.filter(member_id=member).count()
        my_group_count = ReadingGroup.objects.filter(member=member).count()
        
    except Member.DoesNotExist:
        return redirect(f'/member/login/?next={request.path}')  # 세션은 있는데 유저가 없을 경우도 예외 처리

    page = request.GET.get('page', 1)
    qs = Bookmark.objects.filter(member_id=member).order_by('-marked_date')  # member_id는 FK니까 객체로 필터

    paginator = Paginator(qs, 12)
    paginated_bookmarks = paginator.get_page(page)

    context = {
        'bookmarks': paginated_bookmarks,
        'page': int(page),
        'my_review_count': my_review_count,
        'my_bookmark_count': my_bookmark_count,
        "my_group_count": my_group_count,
        "user_id":user_id,
        'review_count':review_count
        
    }
    
    return render(request,'mypage/Bmark.html',context)

def mygroup(request):
    review_count = Review.objects.count()
    user_id = request.session.get('user_id')  # 로그인된 유저의 ID

    if not user_id:
        return redirect(f'/member/login/?next={request.path}')  # 로그인 안 되어있으면 로그인 페이지로

    try:
        member = Member.objects.get(id=user_id)  # 문자열 ID 기준으로 조회
        my_review_count = Review.objects.filter(member_id=member).count()
        my_bookmark_count = Bookmark.objects.filter(member_id=member).count()
        my_group_count = ReadingGroup.objects.filter(member=member).count()
    except Member.DoesNotExist:
        return redirect(f'/member/login/?next={request.path}')  # 세션은 있는데 유저가 없을 경우도 예외 처리

    page = request.GET.get('page', 1)
    qs = ReadingGroup.objects.filter(member=member).order_by('-created_at')  # member_id는 FK니까 객체로 필터
    for g in qs:
            g.membercount = g.member.count()
    paginator = Paginator(qs,8)
    paginated_sharegroups = paginator.get_page(page)

    context = {
        'sharegroups': paginated_sharegroups,
        'page': int(page),
        'my_review_count': my_review_count,
        'my_bookmark_count': my_bookmark_count,
        "my_group_count": my_group_count,
        "user_id":user_id,
        'review_count':review_count,
        
        
    }
    
    
    return render(request,'mypage/mygroup.html',context)


#---------------------------------------------------------------------------

def review_delete(request):
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        if not review_id:
            return JsonResponse({'result': 'error', 'message': '리뷰 ID 없음'}, status=400)

        print("삭제 요청 review_id:", review_id)

        try:
            review_id = int(review_id)  # 문자열을 숫자로 변환
            review = Review.objects.get(review_id=review_id)
            review.delete()
            return JsonResponse({"result": "success"})
        except ValueError:
            return JsonResponse({"result": "error", "message": "리뷰 ID 형식이 잘못되었습니다."}, status=400)
        except Review.DoesNotExist:
            return JsonResponse({"result": "error", "message": "리뷰가 존재하지 않습니다."}, status=404)

    return JsonResponse({'result': 'error', 'message': '허용되지 않은 요청 방식입니다.'}, status=400)



def bookmark_delete(request):
    if request.method == 'POST':
        bookmark_id = request.POST.get('bookmark_id')
        if not bookmark_id:
            return JsonResponse({'result': 'error', 'message': '북마크 ID 없음'}, status=400)

        print("삭제 요청 bookmark_id:", bookmark_id)

        try:
            bookmark_id = int(bookmark_id)  # 문자열을 숫자로 변환
            bookmark = Bookmark.objects.get(bookmark_id=bookmark_id)
            bookmark.delete()
            return JsonResponse({"result": "success"})
        except ValueError:
            return JsonResponse({"result": "error", "message": "북마크 ID 형식이 잘못되었습니다."}, status=400)
        except Bookmark.DoesNotExist:
            return JsonResponse({"result": "error", "message": "북마크가 존재하지 않습니다."}, status=404)

    return JsonResponse({'result': 'error', 'message': '허용되지 않은 요청 방식입니다.'}, status=400)


def mygroup_delete(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        if not id :
            return JsonResponse({'result': 'error', 'message': '그룹 ID 없음'}, status=400)

        print("삭제 요청 id :", id)

        try:
            id = int(id)  # 문자열을 숫자로 변환
            sharegroup = ReadingGroup.objects.get(id=id)
            sharegroup.delete() 
            return JsonResponse({"result": "success"})
        except ValueError:
            return JsonResponse({"result": "error", "message": "그룹 ID 형식이 잘못되었습니다."}, status=400)
        except ReadingGroup.DoesNotExist:
            return JsonResponse({"result": "error", "message": "그룹이 존재하지 않습니다."}, status=404)

    return JsonResponse({'result': 'error', 'message': '허용되지 않은 요청 방식입니다.'}, status=400)
    
        
# def mygroup_delete(request):
#     if request.method == 'POST':
#         print("💬 POST 데이터:", request.POST)

#     group_id = request.POST.get('group_id')  # 띄어쓰기 제거했음

#     if not group_id:
#         return JsonResponse({'result': 'error', 'message': '그룹 ID 없음'}, status=400)

#     print("✅ 삭제 요청 group_id:", group_id)



@csrf_exempt
def member_delete(request):
    if request.method == 'POST':
        # 로그인 여부 확인
        member_id = request.session.get('member_id')
        if not member_id:
            return JsonResponse({'result': 'error', 'message': '로그인 정보가 없습니다.'}, status=401)

        try:
            member = Member.objects.get(member_id=member_id)
            member.delete()
            request.session.clear()  # 세션 초기화 (로그아웃 효과)
            return JsonResponse({'result': 'success', 'message': '계정이 삭제되었습니다.'})
        except Member.DoesNotExist:
            return JsonResponse({'result': 'error', 'message': '회원 정보를 찾을 수 없습니다.'}, status=404)
    else:
        return JsonResponse({'result': 'error', 'message': 'POST 요청만 허용됩니다.'}, status=400)