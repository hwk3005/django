from django.shortcuts import render
from board.models import Board

def list(request):
    qs = Board.objects.order_by('-bgroup','bstep')
    context = {"list":qs}
    return render(request,'board/list.html',context)