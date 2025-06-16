from django.shortcuts import render
# ajax전송에 필요한 선언
from django.http import JsonResponse


# 4. ajax 데이터 전송 - get,post
def view2(request):
    # html에서 데이터 전달
    id = request.POST.get('id','')
    name = request.POST.get('name','')
    # QuerySet, QueryList -> list타입
    # models db데이터가 있으면, list타입으로 변경후 전송해야 함.
    
    # 데이터를 html전송
    context = {'id':id,'name':name,'result':'success','pw':'1111'}
    
    return JsonResponse(context)

# 1. form 데이터 전송 - get,post
def view(request):
    # html에서 데이터 전달
    id = request.POST.get('id','')
    name = request.POST.get('name','')
    # 데이터를 html전송
    context = {'id':id,'name':name}
    return render(request,'board/view.html',context)

def list(request):
    return render(request,'board/list.html')
