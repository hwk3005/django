from django.shortcuts import render
from member.models import Member  #Member테이블 호출

# 로그아웃 부분
def logout(request):
    # session 모두 삭제
    request.session.clear()
    context = {'msg':-1}
    return render(request,'member/login.html',context)


# 로그인 부분
def login(request):
    # 쿠키 읽어오기
    cookie_info = request.COOKIES
    # 있으면 :aaa, 없으면 None -> '' 빈공백처리
    cook_id = request.COOKIES.get('cookie_val','')  
    print("cook_id : ",cook_id)
    context = {'cookie_info':cookie_info, 'cook_id':cook_id}
    
    if request.method == 'GET':  # 로그인페이지 열기
        return render(request,'member/login.html',context)
    # 아이디저장 체크박스
    elif request.method == 'POST': # ID,PW확인
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        cookie_val = request.POST.get('cookie_val')
        
        # 쿠키저장
        
        # id,pw확인 - 없을때 error발생 예외처리
        try:
            qs = Member.objects.get(id=id,pw=pw)
            ## session 추가
            request.session['session_id'] = qs.id
            request.session['session_nickName'] = qs.nickName
            msg = 1  # id,pw가 있음.
            print("데이터 여부 : 존재함")
        except:
            msg = 0  # id,pw가 없음.
            print("데이터 여부 : 없음")
        
        context = {"msg":msg, 'cookie_info':cookie_info,'cook_id':cook_id}
        
        response = render(request,'member/login.html',context)
        # response 쿠키저장
        if cookie_val is not None:
            #cookie_val = 'idsave' 60초*60분*24시간*365일
            response.set_cookie('cookie_val',id,max_age=60*60*24*365)  
        else:
            response.delete_cookie('cookie_val')
        
        return response
    
        
        