from django.shortcuts import render
from django.http import JsonResponse
from comment.models import Comment
from member.models import Member
from board.models import Board

## 하단댓글 수정저장
def cupdate(request):
    cno = request.POST.get('cno')
    ccontent = request.POST.get('ccontent')
    print('넘어온 cno : ',cno,ccontent)
    # db수정저장
    qs = Comment.objects.get(cno=cno)
    qs.ccontent = ccontent
    qs.save()
    # json타입으로 변경
    json_qs = list(Comment.objects.filter(cno=cno).values())
    context = {'result':'success','comment':json_qs} 
    return JsonResponse(context)

## 하단댓글 삭제
def cdelete(request):
    cno = request.POST.get('cno')
    print('넘어온 cno : ',cno)
    # db삭제
    Comment.objects.get(cno=cno).delete()
    
    context = {'result':'success'}
    return JsonResponse(context)


## 하단등록 - Json타입리턴
def cwrite(request):
    # html에서 디장고로 데이터 전달
    id = request.POST.get('id')
    bno = request.POST.get('bno')
    cpw = request.POST.get('cpw','')
    ccontent = request.POST.get('ccontent')
    print('넘어온 데이터 : ',id,cpw,ccontent)
    # id -> member, bno -> board
    member = Member.objects.get(id=id)
    board = Board.objects.get(bno=bno)
    
    # db저장
    qs = Comment.objects.create(member=member,board=board,cpw=cpw,ccontent=ccontent)
    print(qs) #QuerySet타입
    
    # Json타입변경 - QuerySet List타입은 list타입으로 바로 변경
    json_qs = list(Comment.objects.filter(cno=qs.cno).values())
    print(json_qs)
    context = {'result':'success','comment':json_qs}
    return JsonResponse(context)


## 하단댓글리스트 - Json타입리턴
def clist(request):
    context = {'result':'success'}
    return JsonResponse(context)
