from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.core import serializers # json타입으로 변경
from django.views.decorators.csrf import csrf_exempt #csrf토큰이 없을때 예외처리
from board.models import Board

# form게시판 - get,post
def list(request):
    #db 데이터 모두가져오기
    qs = Board.objects.all().order_by('-ntchk','-bgroup','bstep')
    context = {'list':qs} # html전달
    return render(request,'board/list.html',context)
    