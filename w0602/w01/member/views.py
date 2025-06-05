from django.shortcuts import render,redirect
from member.models import Member

### 회원가입 03 - 가입완료
def join03(request):
    return render(request,'member/join03.html')

### 회원가입 02 - 회원가입페이지, 회원가입저장
def join02(request):
    if request.method == 'GET': # 회원가입페이지
        return render(request,'member/join02.html')
    
    elif request.method == 'POST': #회원가입저장
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        name = request.POST.get('name')
        nickName = request.POST.get('nickName')
        f_tell = request.POST.get('f_tell')
        m_tell = request.POST.get('m_tell')
        l_tell = request.POST.get('l_tell')
        tel = f"{f_tell}-{m_tell}-{l_tell}"
        gender = request.POST.get('gender')
        hobby = request.POST.getlist('hobby')
        hobby = ','.join(hobby)
        # db저장
        Member(id=id,pw=pw,name=name,nickName=nickName,tel=tel,gender=gender,hobby=hobby).save()
        
        print("넘어온 데이터 : ",id,pw,name,nickName,tel,gender,hobby)
        
        return redirect('/member/join03/')

### 회원가입 01 - 동의페이지
def join01(request):
    return render(request,'member/join01.html')

#-----------------------------------------------------------------
def logout(request):
    # session 모두삭제
    request.session.clear()
    context = {'msg':-1}
    return render(request,'member/login.html',context)


### login페이지연결, login확인
def login(request):
    if request.method == 'GET':
        # idCheck쿠키를 읽어와서 있으면, 저장된 아이디를 리턴해서 돌려줌.
        # 모든 쿠키 읽어오기 request.COOKIES
        print("모든 쿠키 : ",request.COOKIES)
        # 해당쿠키 읽어오기
        idCheck = request.COOKIES.get('idCheck','') # 없으면 ''빈공백 처리
        context = {'save_id':idCheck}
        return render(request,'member/login.html',context)
    elif request.method == 'POST':
        id = request.POST.get('id') #아이디
        pw = request.POST.get('pw') #패스워드
        idCheck = request.POST.get('idCheck') # 있을수도 있고, 없을수도 있고
        
        # 로그인체크
        try:
            qs = Member.objects.get(id=id,pw=pw)
        except:
            context = {'msg':0}
            return render(request,'member/login.html',context)
            
        # session 저장
        request.session['session_id'] = id
        request.session['session_nickName'] = qs.nickName
                
        # response 쿠키 저장
        context = {'msg':1}
        response = render(request,'member/login.html',context)
        if idCheck != None: # idCheck값이 있으면 - max_age = 60초*60분*24시간*365일
            response.set_cookie('idCheck',id,max_age=60*60) #쿠키저장
        else:
            response.delete_cookie('idCheck') #쿠키삭제
        return response
        
