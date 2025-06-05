from django.shortcuts import render,redirect
from board.models import Board
from django.core.paginator import Paginator
from django.db.models import F,Q

# 글수정페이지, 글수정저장
def update(request,bno):
    if request.method == 'GET': #글수정페이지
        qs = Board.objects.get(bno=bno)  #1개 게시글가져오기
        context = {"board":qs}
        return render(request,'board/update.html',context)
    
    elif request.method == "POST": # 글수정저장
        # 변경된 게시글 가져오기 - 몇 게시글 수정이야?
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        # 1.변경할 게시글 가져오기 - 2.변경된 내용 게시글 저장
        qs = Board.objects.get(bno=bno)
        qs.btitle = btitle
        qs.bcontent = bcontent
        qs.save()
        context = {'msg': 1}   # 글수정저장성공
        return render(request,'board/update.html',context)


# 상세보기
def view(request,bno):
    qs = Board.objects.get(bno=bno)
    context = {'board':qs}
    return render(request,'board/view.html',context)


# 쓰기페이지, 쓰기 저장
def write(request):
    if request.method == 'GET': # 글쓰기페이지
        return render(request,'board/write.html')
    elif request.method == 'POST': # 글쓰기 저장
        id = 'aaa'
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile = request.POST.get('bfile')
        # DB저장후 qs변수로 다시 리턴받음.
        qs = Board.objects.create(id=id,btitle=btitle,bcontent=bcontent)
        qs.bgroup = qs.bno
        qs.save()
        print('데이터 확인 : ',btitle,bcontent,bfile)
        print('데이터추가 : ',qs.bgroup,qs.bstep,bfile)
        return redirect('board:list')
        

# 게시판리스트
def list(request):
    category = request.GET.get('category','')
    search = request.GET.get('search','')
    print("list 넘어온 데이터 : ",category,search)
    page = int(request.GET.get('page',1)) #현재페이지 가져오기
    
    if search != '':
        # 모든 데이터 가져오기
        qs = Board.objects.order_by('-bgroup','bstep')
        # 페이지처리
        paginator = Paginator(qs,5) #페이지처리 100개게시글 -> 10씩 나눔
        list = paginator.get_page(page) #해당페이지 가져오기 -> 10개중에 해당하는 1개 가져오기
        context = {'list':list,'page':page}
        return render(request,'board/list.html',context)
    else:
        # 검색된 데이터 가져오기
        qs = Board.objects.filter(
           Q(btitle__contains=search) | Q(bcontent__contains=search) 
            ).order_by('-bgroup','bstep')
        # 페이지처리
        paginator = Paginator(qs,5) #페이지처리 100개게시글 -> 10씩 나눔
        list = paginator.get_page(page) #해당페이지 가져오기 -> 10개중에 해당하는 1개 가져오기
        context = {'list':list,'page':page,'category':category,'search':search}
        return render(request,'board/list.html',context)
        