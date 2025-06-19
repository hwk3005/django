from django.shortcuts import render
from chart.models import TotalSales
from django.http import JsonResponse

def chlist2(request):
    return render(request,'chart/chlist2.html')


# ajax으로 json타입으로 리턴
def chajax(request):
    aYear = request.POST.get('aYear')
    print('넘어온 aYear : ',aYear)
    # db불러오기 - 하단댓글때 qs list타입변경
    qs = TotalSales.objects.filter(year=aYear)
    print('qs 기본구문 : ',qs)                  # 타입 : QuerySet List타입
    print('list타입 구문 : ',list(qs.values())) # 타입 : List타입
    # json타입으로 변경
    context = {'ajaxlist':list(qs.values())}
    return JsonResponse(context)


# 차트페이지 호출
def chlist(request):
    profit = [20, 15, 7, 25, 27, 30]           # 타입 : List타입
    context = {'profit':profit}
    return render(request,'chart/chlist.html',context)
