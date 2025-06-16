from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.db.models import F,Q  # F:검색된모든데이터적용시, Q:또는 검색
from board.models import Board
from member.models import Member
from comment.models import Comment

## 글 상세보기 - 하단댓글포함
def view(request,bno):
    print("넘어온 데이터 : ",bno)
    # 현재글 - list타입
    qs = Board.objects.filter(bno=bno)
    
    # 이전글
    pre_qs = Board.objects.filter(
       Q(ntchk__lte=qs[0].ntchk,bgroup__lt=qs[0].bgroup,bstep__lte=qs[0].bstep)|
       Q(ntchk=qs[0].ntchk,bgroup__lt=qs[0].bgroup)
    ).order_by('-ntchk','-bgroup','bstep').first()
    # 다음글
    next_qs = Board.objects.filter(
       Q(ntchk__gte=qs[0].ntchk,bgroup__gt=qs[0].bgroup,bstep__gte=qs[0].bstep)|
       Q(ntchk__gt=qs[0].ntchk)
    ).order_by('ntchk','bgroup','-bstep').first()
    print('현재글 : ',qs[0].bno)
    #print('이전글 : ',pre_qs.bno)
    #print('다음글 : ',next_qs.bno)
    
    # 하단댓글 100번 게시글
    c_qs = Comment.objects.filter(board=qs[0]).order_by('-cno')
    print("하단댓글 데이터 : ",c_qs)
    
    context = {'board':qs[0],'pre_board':pre_qs,'next_board':next_qs,'comment':c_qs}
    return render(request,'board/view.html',context)

## 글쓰기 - get,post
def write(request):
    if request.method == 'GET':
        return render(request,'board/write.html')
    elif request.method == 'POST':
        id = request.POST.get('id')
        member = Member.objects.get(id=id)
        # id = request.session.get('session_id') # session에서 가져오기
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile','')
        ntchk = request.POST.get('ntchk',0)
        print("넘어온 데이터 : ",id,btitle,bcontent,bfile,ntchk)
        ### db저장
        qs = Board.objects.create(member=member,btitle=btitle,bcontent=bcontent,bfile=bfile,ntchk=ntchk)
        # 답글달기할때 필요
        qs.bgroup = qs.bno
        qs.save()        
        return redirect('/board/list/')
        

## 게시판리스트
def list(request):
    # 페이지번호가 있어야 함.
    page = int(request.GET.get('page',1))
    qs = Board.objects.all().order_by('-ntchk','-bgroup','bstep')
    # 하단넘버링부분
    paginator = Paginator(qs,10)    # 10개씩 분리해서 가져옴. 1,2,...10페이지생성
    list = paginator.get_page(page) # 1페이지 가져오기 -> 10개 게시글
    # -----------
    context = {'list':list,'page':page}
    return render(request,'board/list.html',context)
