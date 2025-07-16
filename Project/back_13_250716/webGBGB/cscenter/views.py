from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import F,Q
import datetime
from cscenter.models import Notice,Inquiry
from member.models import Member
from django.http import JsonResponse

def list(request):
    # 요청하는 page번호 가져오기, str타입 -> int타입
    page = int(request.GET.get('page',1))
    # search
    search = request.GET.get('search','')
    print('검색 데이터: ',search)

    if search == '':   # 일반리스트로 넘어온 경우
        # 게시글 전체 가져오기
        qs = Notice.objects.order_by('-ntcno')
        # 페이지 분기
        paginator = Paginator(qs,10) # 100->10개씩 쪼개서 전달해줌
        noticeList = paginator.get_page(page)  # 현재페이지에 해당되는 게시글 전달
        context = {'notice':qs,'list':noticeList,'page':page,'search':0}
        return render(request, 'cscenter/list.html', context)
    else:   # 검색으로 넘어온 경우
        # 게시글 전체 가져오기  and:& or:| not:~
        qs = Notice.objects.filter(
            Q(ntitle__contains=search) | Q(ncontent__contains=search)).order_by('-ntcno')
        
        # 페이지 분기
        paginator = Paginator(qs,10)
        noticeList = paginator.get_page(page)
       # 게시글 10개, 현재페이지 보냄
        context = {'notice':qs,'list':noticeList,'page':page,'search':1}
        return render(request,'cscenter/list.html',context)

def view(request,ntcno):
    qs = Notice.objects.filter(ntcno=ntcno)
    
    # 1. 조회수 증가 확인
    # qs.update(nhit=F('nhit')+1) # view페이지에서 보면 곧장 조회수 1 증가함(F함수 사용하면 데이터베이스에 직접 업데이트)
    # print(f"조회수 증가됨: {qs[0].ntcno}")  프롬프트창에서 확인가능
    
    # 2. 중복 조회수 상승 방지(ip 기반, 쿠키 사용)
    user_identifier = request.META.get('REMOTE_ADDR','anonymous')
    cookie_name = f'notice_hit_{user_identifier}'
    
    # 하루 마지막 시간에 쿠키 만료
    tomorrow = datetime.datetime.now().replace(hour=23,minute=59,second=59)
    expires = tomorrow.strftime("%a, %d-%b-%Y %H:%M:%S GMT")

    # 쿠키 확인, 조회수 증가
    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        print(f"기존 쿠키: {cookies}")
        cookies_list = cookies.split('|')
        
        if str(ntcno) not in cookies_list:
            qs.update(nhit=F('nhit')+1)
            qs[0].refresh_from_db()
            new_cookie_val = cookies + f"|{ntcno}"
        else: new_cookie_val = cookies
    
    else:
        qs.update(nhit=F('nhit')+1)
        qs[0].refresh_from_db()
        new_cookie_val = str(ntcno)
        
    # 다음글: ntcno가 현재글보다 큰것 중 가장 작은거(역순정렬했을때 바로 위글)
    next_qs = Notice.objects.filter(ntcno__gt = qs[0].ntcno).order_by('ntcno').first()
    
    # 이전글: ntcno가 현재글보다 작은것 중 가장 큰거(역순정렬했을때 바로 아래글)
    pre_qs = Notice.objects.filter(ntcno__lt = qs[0].ntcno).order_by('-ntcno').first()
    
    context={'notice':qs[0],'next_ntc':next_qs,'pre_ntc':pre_qs}
    response = render(request,'cscenter/view.html',context)
    response.set_cookie(cookie_name, new_cookie_val, expires=expires)
    return response

def inquiry(request):
    if request.method == 'GET':
        return render(request, 'cscenter/inquiry.html')

    elif request.method == 'POST':
        return redirect('/cscenter/notice/')
    


@require_http_methods(["POST"])
def submit(request):
    try:
        category = request.POST.get('category_inq')
        title = request.POST.get('title_inq')
        content = request.POST.get('content_inq')
        
        # 업로드된 파일s 처리
        uploaded_files = []
        for key, file in request.FILES.items():
            if key.startswith('uploaded_file_'):
                uploaded_files.append(file)
        
        # 모델에 저장 (파일 필드가 어떻게 정의되어 있는지에 따라 다름)
        id=request.session['user_id']
        
        inquiry = Inquiry.objects.create(
            ictgr=category,
            ititle=title,
            icontent=content,
            member=Member.objects.get(id=id),
        )
        
        # 파일들을 별도로 저장 (파일 개수에 상관없이)
        for i, file in enumerate(uploaded_files[:3]):  # 최대 3개까지만
            if i == 0:
                inquiry.ifile1 = file
            elif i == 1:
                inquiry.ifile2 = file
            elif i == 2:
                inquiry.ifile3 = file
        
        inquiry.save()
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})