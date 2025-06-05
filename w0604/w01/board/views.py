from django.shortcuts import render,redirect
from board.models import Board
# F : 검색된 필드에서 특정컬럼의 값을 가져올때
# Q : and,or,not 연산을 사용할때 
from django.db.models import F,Q
from django.core.paginator import Paginator

# 답글달기 - 답글달기페이지열기, 답글달기저장
def reply(request,bno):
    if request.method == 'GET':
        qs = Board.objects.get(bno=bno)
        context = {'board':qs}
        return render(request,'board/reply.html',context)
    elif request.method == 'POST':
        id = request.POST.get("id") #session_id 가져옴.
        bgroup = request.POST.get("bgroup")  # 부모의 bgroup
        bstep = int(request.POST.get("bstep")) # 부모의 bstep
        bindent = int(request.POST.get("bindent")) #부모의 bindent
        btitle = request.POST.get("btitle")
        bcontent = request.POST.get("bcontent")
        bfile = request.FILES.get("bfile",'')
        
        ### 답글달기저장
        # 1.  gt, lt, gte, lte 언더바 2개 넣어야 함.
        # 부모보다 bstep 더 큰것, 모든자식들은 전부 bstep을 1씩 증가시켜야 함.
        # F함수 현재 찾아진 컬럼의 값을 모두 가져옴.
        reply_qs = Board.objects.filter(bgroup=bgroup,bstep__gt=bstep)
        reply_qs.update(bstep = F('bstep')+1)
        # 2. db저장
        qs = Board.objects.create(id=id,btitle=btitle,bcontent=bcontent,
            bgroup=bgroup,bstep=bstep+1,bindent=bindent+1,bfile=bfile)
        print('')        
        context = {"msg":1,'board':qs}
        return render(request,'board/reply.html',context)
        


# 게시글 삭제
def delete(request,bno):
    ## 게시글 삭제
    Board.objects.get(bno=bno).delete()    
    return redirect('/board/list/')


# 게시글수정 - 업데이트페이지열기, 업데이트저장
def update(request,bno):
    if request.method == 'GET':
        qs = Board.objects.get(bno=bno)
        context = {'board':qs}
        return render(request,'board/update.html',context)
    elif request.method == 'POST':
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile_pre = request.POST.get('bfile_pre','')
        bfile = request.FILES.get('bfile','') # 파일업로드
        if not bfile:
            bfile = bfile_pre
        qs = Board.objects.get(bno=bno)
        qs.btitle = btitle
        qs.bcontent = bcontent
        qs.bfile = bfile
        qs.save()
        context = {'msg':1,'board':qs}
        return render(request,'board/update.html',context)
        


# 게시글쓰기 - 게시글페이지열기, 게시글저장
def write(request):
    if request.method == "GET":
        return render(request,'board/write.html')
    elif request.method == "POST":
        # 데이터 가져오기
        id = request.POST.get('id') #섹션에서 가져옴.
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        # bfile = request.POST.get('bfile')
        bfile = request.FILES.get('bfile','')
        print('파일부분 : ',request.FILES)
        print('bfile 가져온 데이터 : ',bfile)
        # 1.save() 저장
        # Board(id=id,btitle=btitle,bcontent=bcontent,bfile=bfile).save()
        # 2.create저장
        qs = Board.objects.create(id=id,btitle=btitle,bcontent=bcontent,bfile=bfile)
        qs.bgroup = qs.bno
        qs.save()
        context = {'msg':1}
        return render(request,'board/write.html',context)

# 게시글보기
def view(request,bno):
    # 1.qs값 수정
    # qs = Board.objects.get(bno=bno)
    # qs.bhit += 1
    # qs.save()
    # context = {'board':qs}
    
    # 2.F함수사용 - filter검색후, 특정컬럼의 값을 가져오는 함수
    category = request.GET.get('category','')
    search = request.GET.get('search','')
    
    qs = Board.objects.filter(bno=bno) # 리스트
    qs.update(bhit = F('bhit')+1) #save까지 됨.
    context = {'board':qs[0],'category':category,'search':search}
    
    return render(request,'board/view.html',context)



# 게시판리스트 - 일반게시판리스트, 검색게시판리스트
def list(request):
    # 현재페이지 int변경
    page = int(request.GET.get('page',1)) # 없을때, 1페이지로 넘겨줌
    #search으로 넘어올때
    search = request.GET.get('search','') 
    category = request.GET.get('category','')
    print('검색데이터 : ',category,search)
    
    if search == '':  # 일반리스트로 넘어온 경우
        # 게시글 전체 가져오기
        qs = Board.objects.order_by('-bgroup','bstep')
        # 페이지 분기
        paginator = Paginator(qs,20) # 100개 -> 10개씩 쪼개서 전달해줌.
        list = paginator.get_page(page)  # 현재페이지에 해당되는 게시글 전달
        context = {"list":list,'page':page}
        return render(request,'board/list.html',context)
    else:            # 검색으로 넘어온 경우
        # 게시글 전체 가져오기  and:& or:| not:~
        if category == 'all':
            qs = Board.objects.filter(
                Q(btitle__contains=search) | Q(bcontent__contains=search))
        elif category == 'btitle':
            qs = Board.objects.filter(btitle__contains=search)
        else:
            qs = Board.objects.filter(bcontent__contains=search)
        
        # 페이지 분기
        paginator = Paginator(qs,20) # 100개 -> 10개씩 쪼개서 전달해줌.
        list = paginator.get_page(page)  # 현재페이지에 해당되는 게시글 전달
        context = {"list":list,'page':page,'category':category,'search':search}
        return render(request,'board/list.html',context)
        
    
    
        
