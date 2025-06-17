from django.shortcuts import render
from django.http import JsonResponse
from member.models import Member

# id중복확인
def idchk(request):
    id = request.POST.get('id','')
    print('넘어온 id : ',id);
    ## DB확인 - Member테이블
    try:
        qs = Member.objects.get(id=id)
        print(qs)
        result = 1
    except:
        result = 0    
     
    print("확인 : ",result)       
    context = {'result':result}
    return JsonResponse(context)

def step04(request):
    return render(request,'member/step04.html')

## get-페이지호출, post-회원정보저장
def step03(request):
    if request.method == 'GET':
        return render(request,'member/step03.html')
    elif request.method == 'POST' :
        # 회원정보 DB저장
        name = request.POST.get('name')
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        email1 = request.POST.get('email1')
        email2 = request.POST.get('email2')
        email = f'{email1}@{email2}' #
        emailc = request.POST.get('emailc')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        address3 = request.POST.get('address3')
        phone1 = request.POST.get('phone1') 
        phone2 = request.POST.get('phone2')
        phone3 = request.POST.get('phone3')
        phone = f'{phone1}-{phone2}-{phone3}'#
        tel1 = request.POST.get('tel1')
        tel2 = request.POST.get('tel2')
        tel3 = request.POST.get('tel3')
        tel = f'{tel1}-{tel2}-{tel3}'#
        birth1 = request.POST.get('birth1')
        birth2 = request.POST.get('birth2')
        birth3 = request.POST.get('birth3')
        birth = f'{birth1}-{birth2}-{birth3}' #
        corporate = request.POST.get('corporate')
        gender = request.POST.get('gender')
        hobby = request.POST.getlist('hobby')
        Member.objects.create(name=name,id=id,pw=pw,email=email,
                              emailc=emailc,address1=address1,address2=address2,
                              address3=address3,phone=phone,
                              tel=tel,birth=birth,corporate=corporate,
                              gender=gender,hobby=hobby
                              )
        print('회원정보 저장')
        # 이메일 보내는 소스코드 추가
        
        
        context = {'name':name,'id':id,'email':email}
        return render(request,'member/step04.html',context)
        

def step02(request):
    return render(request,'member/step02.html')

def step01(request):
    return render(request,'member/step01.html')
