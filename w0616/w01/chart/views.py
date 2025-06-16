from django.shortcuts import render
from chart.models import TotalSales

# 차트페이지 호출
def chlist(request):
    profit = [20, 15, 7, 25, 27, 30]           # 타입 : List타입
    qs = TotalSales.objects.filter(year=2025)
    print('qs 기본구문 : ',qs)                  # 타입 : QuerySet List타입
    print('list타입 구문 : ',list(qs.values())) # 타입 : List타입
    context = {'profit':profit,'list':qs,'list_list':list(qs.values())}
    print("영업이익 : ",profit)
    return render(request,'chart/chlist.html',context)
