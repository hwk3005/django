from django.shortcuts import render, redirect
from . models import ReadingGroup  # 그룹 모델
from django.views.decorators.csrf import csrf_exempt


# 교환독서_그룹만들기 | Share_AddGroup
# @csrf_exempt  # 임시로 CSRF 막기 (실제 배포할 땐 csrf_token 꼭 쓰기!)
def Share_AddGroup(request):
    if request.method == 'GET':
        return render(request,'shareMain/Share_AddGroup.html')
    elif request.method == 'POST' :
        # 회원정보 DB저장
        group_name = request.POST.get('group_name')
        member_count = int(request.POST.get('member_count',2))
        description = request.POST.get('description')
        book = request.POST.get('book')
        tag = request.POST.get('tag')
        is_public = int(request.POST.get('is_public',0))
        password = request.POST.get('password')
    
        ReadingGroup.objects.create(
            group_name=group_name,
            member_count=member_count,
            description=description,
            book=book,
            tag=tag,
            is_public=is_public,
            password=password,
        )
        print("그룹 저장 완료")
        
        # 방법 1: render로 context 전달
        groups = ReadingGroup.objects.all()
        
        context = {'groups': groups,'tag':tag,'group_name':group_name,'book':book }
        return render(request, 'shareMain/Share_Main.html', context)




# 교환독서_메인페이지 | Share_Main
def Share_Main(request):
    groups = ReadingGroup.objects.all()
    
    context = {'groups':groups}
    return render(request, 'shareMain/Share_Main.html', context)
