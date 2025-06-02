from django.shortcuts import render, redirect
from member.models import Member

### login 
# 순서 1 ;
def login(request):
    if request.method == 'GET':
        print("모든 쿠키: ",request.COOKIES)
        idCheck = request.COOKIES.get('idCheck','')
        context = {'save_id':idCheck}
        return render(request,'member/login.html', context)
    elif request.method == 'POST':
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        idCheck = request.POST.get('idCheck')
        
        # 순서 3 ; 로그인체크
        try:
            qs = Member.objects.get(id=id,pw=pw)
        except:
            context = {'msg':0}
            return render(request,'member/login.html',context)
        
        # 순서 4 ; session 저장
        request.session['session_id'] = id
        request.session['session_nickName'] = qs.nickName
        
        # 순서 2 ; response 쿠키 저장
        context = {'msg':1}
        response = render(request,'member/login.html',context)
        if idCheck != None:  # idCheck값이 있으면
            response.set_cookie('idCheck',id,max_age=60*60)  # 쿠키저장
        else:
            response.delete_cookie('idCheck')  # 쿠키삭제
        return response