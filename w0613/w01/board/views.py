from django.shortcuts import render
from board.models import Board
from comment.models import Comment

## 게시판 뷰페이지
def view(request,bno):
    # db에서 가져오기
    qs = Board.objects.get(bno=bno)
    c_qs = Comment.objects.filter(board=qs).order_by('-cno')  # 3개
    context = {'board':qs,'clist':c_qs}
    return render(request,'board/view.html',context)

## 게시판리스트
def list(request):
    # db에서 가져오기
    qs = Board.objects.all().order_by('-ntchk','-bgroup','bstep')
    context = {'list':qs}
    return render(request,'board/list.html',context)
