from django.shortcuts import render, redirect
from . models import ReadingGroup  # 그룹 모델
from django.views.decorators.csrf import csrf_exempt


# 교환독서_그룹만들기 | Share_AddGroup
@csrf_exempt  # 임시로 CSRF 막기 (실제 배포할 땐 csrf_token 꼭 쓰기!)
def Share_AddGroup(request):
    if request.method == 'POST':
        name = request.POST.get('group_name	')
        member_count = request.POST.get('member_count')
        desc = request.POST.get('description')

        ReadingGroup.objects.create(
            name=name,
            member_count=member_count,
            description=desc
        )
        return redirect('/Share_Main/')  # 생성 후 목록 페이지로 이동
    return render(request, 'shareMain/Share_AddGroup.html')  # GET 요청 시 폼 띄우기





# 교환독서_메인페이지 | Share_Main
def Share_Main(request):
    groups = ReadingGroup.objects.all()
    
    context = {'groups':groups}
    return render(request, 'shareMain/Share_Main.html', context)
