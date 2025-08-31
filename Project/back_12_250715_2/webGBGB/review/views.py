from django.shortcuts import render, redirect
from review.models import Review, ReviewLike, ReviewImage
from member.models import Member
from booksearch.models import Book
from django.contrib import messages
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect


# Create your views here.
def review_create(request):
    if request.method == 'POST':
        member_id = request.session.get('user_id')
        member = Member.objects.get(id=member_id)  # Member 객체 가져오기


        book_id = request.POST.get('book_id')
        try:
            book = Book.objects.get(book_id=book_id)  # Book 객체 가져오기
        except Book.DoesNotExist:
            messages.error(request, "책 정보가 없습니다.")
            return redirect('/')

        rating = int(request.POST.get('rating', 0))
        tag = request.POST.get('tag', '')
        comments = request.POST.get('reviewText', '')

        review = Review.objects.create(
            member_id=member,
            book_id=book,
            rating=rating,
            tag=tag,
            content=comments,
        )
        
        book.review_count += 1
        book.rating += rating
        book.save()

        print("넘어온 데이터 : ", member_id, book_id, rating, tag, comments)
                
        images = request.FILES.getlist('review_image', '')  # 단일 이미지 (ImageField 단일)
        for i, img in enumerate(images):
            if i>=3:
                break
            ReviewImage.objects.create(review_id=review, image=img)

        print("FILES:", request.FILES)
        print("IMAGES:", request.FILES.getlist('review_image'))

        # 리뷰 저장 후
        return redirect(f'/booksearch/detail/{book.book_id}/')

def review_delete(request, review_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('/member/login/')

    member = Member.objects.get(id=user_id)
    review = Review.objects.get(review_id=review_id)
    
    rating = review.rating
    book = review.book_id
        
    print(review.member_id, member.member_id)
    review.delete()
    
    book.review_count = max(0, book.review_count - 1)
    book.rating = max(0, book.rating - rating)
    book.save()
    
    messages.success(request, "리뷰가 삭제되었습니다.")
    
    return redirect(f'/booksearch/detail/{review.book_id.book_id}/')

@csrf_protect
@require_POST
def review_like(request):
    user_id = request.session.get('user_id')
    try:
        member = Member.objects.get(id=user_id)
    except Member.DoesNotExist:
        return JsonResponse({'error': '회원 정보가 없습니다.'}, status=404)

    try:
        data = json.loads(request.body)
        review_id = data.get('review_id')
    except Exception:
        return JsonResponse({'error': '잘못된 요청 데이터입니다.'}, status=400)

    try:
        review = Review.objects.get(pk=review_id)
    except Review.DoesNotExist:
        return JsonResponse({'error': '리뷰 정보가 없습니다.'}, status=404)

    # 좋아요 토글
    like_obj, created = ReviewLike.objects.get_or_create(member_id=member, review_id=review)
    if not created:
        # 이미 좋아요 누른 상태 -> 취소
        like_obj.delete()
        review.likes = max(0, review.likes - 1)
        review.save()
        liked = False
    else:
        # 좋아요 추가
        review.likes += 1
        review.save()
        liked = True

    return JsonResponse({'liked': liked, 'likes': review.likes})

def review_update(request):
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
        
        book_id = request.POST.get('book_id')
        try:
            book = Book.objects.get(book_id=book_id)
        except Book.DoesNotExist:
            messages.error(request, "책 정보가 없습니다.")
            return redirect('/')

        review_id = request.POST.get('review_id', '')
        rating = int(request.POST.get('rating', 0))
        tag = request.POST.get('tag', '')
        comments = request.POST.get('reviewText', '')

        review = Review.objects.get(review_id=review_id)

        # 1. 기존 이미지를 클라이언트가 남기기로 한 목록만 유지
        #    (hidden input으로 넘어온 기존 이미지 파일명/경로)
        existing_images = request.POST.getlist('existing_images')  # ['img1.jpg', ...]

        # 2. 현재 DB에 저장된 모든 이미지 목록
        db_images = ReviewImage.objects.filter(review_id=review)

        # 3. DB에 있는데 클라이언트가 남기지 않은 이미지는 삭제
        for db_img in db_images:
            # db_img.image.name 또는 db_img.image.url (필요에 따라)
            if db_img.image.name not in existing_images and db_img.image.url not in existing_images:
                db_img.delete()

        # 4. 새로 업로드된 이미지 저장 (최대 3장까지)
        images = request.FILES.getlist('modify_review_image')
        # 현재 남아있는 이미지 개수
        current_img_count = ReviewImage.objects.filter(review_id=review).count()
        for i, img in enumerate(images):
            if current_img_count + i >= 3:
                break
            ReviewImage.objects.create(review_id=review, image=img)

        # 평점 갱신
        book.rating -= review.rating
        review.rating = rating
        review.tag = tag
        review.content = comments
        review.save()
        book.rating += rating
        book.save()

        print("넘어온 데이터 : ", member_id, book_id, rating, tag, comments, images, existing_images)

        return redirect(f'/booksearch/detail/{book.book_id}/')
