from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from customer.models import Customer
from member.models import Member
from comment.models import Comment
import datetime
from django.db.models import F


# 게시글 수정 get:수정페이지, post:수정저장
def update(request,bno):
    if request.method == 'GET':
        qs = Customer.objects.get(bno=bno)
        context = {'customer':qs}
        return render(request,'customer/update.html',context)
    
    elif request.method == 'POST':
        # db가져오기
        qs = Customer.objects.get(bno=bno)
        # 넘어온 데이터
        qs.btitle = request.POST.get('btitle')
        qs.bcontent = request.POST.get('bcontent')
        
        # 이미지 파일첨부가 있으면
        if request.FILES.get('bfile'):
            qs.bfile = request.FILES.get('bfile')
            
        # 이미지 파일첨부2가 있으면
        if request.FILES.get('bfile2'):
            qs.bfile2 = request.FILES.get('bfile2')
        
        qs.save()     
        context = {'msg':1,'bno':bno}
        return render(request,'customer/update.html',context)
        


# 게시글 삭제
def delete(request,bno):
    if request.session['session_id']:
        Customer.objects.get(bno=bno).delete()
        context = {'msg':-1}
    else:
        context = {'msg':-2}    
    return render(request,'customer/view.html',context)
    # return redirect('/customer/list/')


# 게시글 상세보기 
# 쿠키 저장형태 : cookie_bhit:aaa  101|102|97|90
def view(request,bno):
  # db연결
  qs = Customer.objects.filter(bno=bno)
  # comment db연결
  c_qs = Comment.objects.filter(customer=qs[0])
  context = {'customer':qs[0],'clist':c_qs}
  response = render(request,'customer/view.html',context)
  
  
  # 쿠키이름 지정 - cookie_bhit:aaa, cookie_bhit:bbb, cookie_bhit:아이디
  cookie_name = f'cookie_bhit:{request.session["session_id"]}'
  
  # 쿠키시간설정 - 1일기준
  #   tomorrow = datetime.datetime.now()  # 현재시간
  # 해당일의 마지막 시간으로 설정
  tomorrow = datetime.datetime.replace(datetime.datetime.now(),
                                       hour=23,minute=59,second=59)
  # 쿠키시간으로 설정형태 변경
  expires = datetime.datetime.strftime(tomorrow,"%a, %d-%b-%Y %H:%M:%S GMT")
  
  if request.COOKIES.get(cookie_name) is not None:
      cookies = request.COOKIES.get(cookie_name) #쿠키가져오기
      print('쿠키 : ',cookies)
      cookies_list = cookies.split('|')  # 101|20|100|97 -> [101,20,100,97]
      # 비교타입 - str타입   cookie_bhit:aaa    103|101
      if str(bno) not in cookies_list:
          response.set_cookie(cookie_name,cookies+f'|{bno}',expires=expires)
          qs.update(bhit=F('bhit')+1) # 조회수1증가
      
  else:
      #  쿠키이름 : cookie_bhit:aaa
      response.set_cookie(cookie_name,bno,expires=expires)
      qs.update(bhit = F('bhit')+1)   # qs.bhit += 1
  
  return response
        
   

# 게시글 쓰기 - get:글쓰기페이지, post:글쓰기저장
def write(request):
    if request.method == 'GET':
        return render(request,'customer/write.html')
    elif request.method == 'POST':
        btitle = request.POST.get('btitle')
        ## session 서버 
        id = request.session['session_id']
        member = Member.objects.get(id=id)
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile','')
        bfile2 = request.FILES.get('bfile2','')
        qs = Customer.objects.create(btitle=btitle,member=member,bcontent=bcontent,bfile=bfile,bfile2=bfile2)
        qs.bgroup = qs.bno
        qs.save()
        print('------------------')
        print(btitle,id,bcontent,bfile,bfile2)
        print('------------------')
        context = {'msg':1}
        return render(request,'customer/write.html',context)
        return render(request,'customer/write.html',context)
        

# 게시판리스트
def list(request):
    # 요청하는 page번호 가져오기, str타입 -> int타입
    page = int(request.GET.get('page',1))
    # db에서 데이터 가져오기
    qs = Customer.objects.all().order_by('-ntchk','-bgroup','bstep')
    # 10개단위로 qs로 분리시킴
    paginator = Paginator(qs,10)
    
    # 가져올 페이지 선택
    customerList = paginator.get_page(page)
    print('-----------------')
    print(customerList)
    print('-----------------')
    
    # 게시글 10개, 현재페이지 보냄
    context = {'list':customerList,'page':page}
    return render(request,'customer/list.html',context)
    # return redirect('/customer/list/')
