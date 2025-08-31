from django.shortcuts import render, redirect
from django.contrib import messages
from member.models import Member
from reply.models import Reply
from booksearch.models import Book
from review.models import Review

# Create your views here.
def reply_create(request):
    if request.method == 'POST':
        member_id = request.session.get('user_id')
        
        member = Member.objects.get(id=member_id)  # Member 객체 가져오기
        
        review_id = request.POST.get('review_id')
        try:
            review = Review.objects.get(review_id=review_id)  # review 객체 가져오기
        except Review.DoesNotExist:
            messages.error(request, "리뷰 정보가 없습니다.")
            return redirect('/')
        
        try:
            book = Book.objects.get(book_id=review.book_id.book_id)
        except Book.DoesNotExist:
            messages.error(request, "책 정보가 없습니다.")
            return redirect('/')
            
        comments = request.POST.get('replyText', '')
        
        Reply.objects.create(
            member_id=member,
            review_id=review,
            content=comments
        )
        review.comments = Review.objects.filter(pk=review.pk).values_list('comments',flat=True)[0]+1
        review.save()
        
        print("넘어온 데이터 : ", member_id, comments)
        
        messages.success(request, "답글이 등록되었습니다.")

        
        return redirect(f'/booksearch/detail/{book.book_id}/')

def reply_delete(request, reply_id):
    user_id = request.session.get('user_id')

    member = Member.objects.get(id=user_id)
    reply = Reply.objects.get(reply_id=reply_id)
    
    if reply.member_id.member_id != member.member_id:
        messages.error(request, "본인이 작성한 리뷰만 삭제할 수 있습니다.")
        return redirect(f'/booksearch/detail/{reply.review_id.book_id.book_id}/')
    
    print(reply.member_id, member.member_id)
    
    review = reply.review_id
    if review.comments > 0:
        review.comments -= 1
        review.save()

    reply.delete()
    
    messages.success(request, "답글이 삭제되었습니다.")
    
    return redirect(f'/booksearch/detail/{reply.review_id.book_id.book_id}/')
        
def reply_modify(request, reply_id):
    user_id = request.session.get('user_id')

    member = Member.objects.get(id=user_id)
    reply = Reply.objects.get(reply_id=reply_id)
    
    if reply.member_id.member_id != member.member_id:
        messages.error(request, "본인이 작성한 리뷰만 수정할 수 있습니다.")
        return redirect(f'/booksearch/detail/{reply.review_id.book_id.book_id}/')
    
    print(reply.member_id, member.member_id)
    
    content=request.POST.get("replymodifycontent", " ")
    
    reply.content = content
    reply.save()
    
    
    return redirect(f'/booksearch/detail/{reply.review_id.book_id.book_id}/')
    