from django.shortcuts import render
from django.http import JsonResponse
from comment.models import Comment

# 하단댓글 삭제
def cdelete(request):
    cno = request.POST.get('cno')
    print('넘어온 cno : ',cno)
    # db삭제처리
    Comment.objects.get(cno=cno).delete()
    
    context = {'msg':'success'}
    return JsonResponse(context)

# 하단댓글리스트
def clist(request):
    context = {}
    return render(request,'customer/list.html',context)

