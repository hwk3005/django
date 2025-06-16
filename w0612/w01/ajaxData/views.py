from django.shortcuts import render
from django.http import JsonResponse
from board.models import Board

# 게시글 삭제
def bdelete(request):
    bno = request.POST.get('bno')
    ## db삭제
    Board.objects.get(bno=bno).delete()
    context = {'result':'success'}
    return JsonResponse(context)

# 게시글 등록
def bwrite(request):
    id = request.POST.get('id')
    btitle = request.POST.get('btitle')
    bcontent = request.POST.get('bcontent')
    # db저장
    qs = Board.objects.create(id=id,btitle=btitle,bcontent=bcontent)
    qs.bgroup = qs.bno
    qs.save()
    # json타입변환
    l_qs = list(Board.objects.filter(bno=qs.bno).values())
    context = {'result':'success','board':l_qs}
    return JsonResponse(context)


# form게시판 - get,post
def blist(request):
    ### db게시글 전체가져오기
    qs = Board.objects.all().order_by('-ntchk','-bgroup','bstep')
    print('queryset타입 : ',qs)
    ### json타입으로 변경
    l_qs = list(qs.values())
    print('리스트타입 : ',l_qs)
    
    context = {'result':'success','list':l_qs}
    return JsonResponse(context)
    
    
    
