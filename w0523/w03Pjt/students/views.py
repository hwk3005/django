from django.shortcuts import render
from django.http import HttpResponse

def list(request):
    return render(request,'list.html')  # html페이지 연결
    # return HttpResponse("리스트페이지 연결") # str 글자 출력
