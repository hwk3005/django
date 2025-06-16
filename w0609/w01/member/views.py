from django.shortcuts import render,redirect
from member.models import Member

# 로그아웃부분
def logout(request):
    request.session.clear()
    context = {'msg':-1}
    return render(request,'member/login.html',context)

# 로그인부분 - get, post
def login(request):
    if request.method == 'GET':
        ## 쿠키 읽어오기
        cook_id = request.COOKIES.get('cook_id','')
        context = {'cook_id':cook_id}
        return render(request,'member/login.html',context)
    elif request.method == 'POST':
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        idsave = request.POST.get('idsave')
        print("로그인 넘어온 데이터 : ",id,pw,idsave)
        ## id,pw확인
        msg = 0
        try:
            qs = Member.objects.get(id=id,pw=pw)
            request.session['session_id'] = id #session id를 추가
            request.session['session_name'] = qs.name #session name를 추가
            msg = 1
        except: print('데이터가 없습니다.')    
        ## 쿠키 읽어오기
        cook_id = request.COOKIES.get('cook_id','')
        context = {'msg':msg,'cook_id':cook_id}
        response = render(request,'member/login.html',context)
        ## 쿠키저장
        if idsave:
            response.set_cookie('cook_id',id,max_age=60*60*24*30)
        else:
            response.delete_cookie('cook_id')    
        return response
   
# 회원가입완료부분
def step04(request,name):
    print("name : ",name)
    context={'name':name}
    return render(request,'member/step04.html',context)        

# 회원가입부분 - get,post
def step03(request):
    if request.method == 'GET':
        return render(request,'member/step03.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        id = request.POST.get('id')
        email1 = request.POST.get('email1')
        email2 = request.POST.get('email2')
        email = f'{email1}@{email2}'
        emailc = request.POST.get('emailc')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        phone1 = request.POST.get('phone1')
        phone2 = request.POST.get('phone2')
        phone3 = request.POST.get('phone3')
        phone = f'{phone1}-{phone2}-{phone2}'
        tel1 = request.POST.get('tel1')
        tel2 = request.POST.get('tel2')
        tel3 = request.POST.get('tel3')
        tel = f'{tel1}-{tel2}-{tel3}'
        birth1 = request.POST.get('birth1')
        birth2 = request.POST.get('birth2')
        birth3 = request.POST.get('birth3')
        birth = f'{birth1}-{birth2}-{birth3}'
        corporate = request.POST.get('corporate')
        gender = request.POST.get('gender')
        hobbys = request.POST.getlist('hobby')
        hobby = ','.join(hobbys)
        print("넘어온 데이터 : ",name,id,email,emailc,address1,address2
              ,phone,tel,birth,corporate,gender,hobby)
        
        ### Member테이블 저장
        Member.objects.create(name=name,id=id,email=email,emailc=emailc,
                    address1=address1,address2=address2,phone=phone,
                    tel=tel,birth=birth,corporate=corporate,
                    gender=gender,hobby=hobby)
        
        return redirect(f'/member/step04/{name}/')
        
    

# 약관동의부분
def step02(request):
    return render(request,'member/step02.html')

# 이메일인증부분
def step01(request):
    return render(request,'member/step01.html')
