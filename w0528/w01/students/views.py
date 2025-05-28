from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from students.models import Student  # Student테이블

# 학생정보 삭제
def delete(request,name):
    print("삭제 이름: ",name)
    qs = Student.objects.get(name=name)  # 해당되는 학생정보검색
    qs.delete()  # 삭제
    return redirect('/students/list')

# 학생정보 수정
def update(request,name):
    if request.method == 'GET':
        print("학생이름: ",name)
        qs = Student.objects.get(name=name)  # 해당되는 학생정보검색
        context = {'stu':qs}
        return render(request,'students/update.html',context)
    else:
        name2 = request.POST.get('name')
        major = request.POST.get('major')
        grade = request.POST.get('grade')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        print("입력된 정보: ",name,major,grade,age,gender)
        ## DB수정
        # 1. 회원검색
        qs = Student.objects.get(name=name)  # 해당되는 학생정보검색
        # 2. 회원정보수정
        qs.name = name2
        qs.major = major
        qs.grade = grade
        qs.age = age
        qs.gender = gender
        # 3. 저장
        qs.save()
        print("Student 객체 수정")
        return redirect('/students/list/')

# 학생정보 상세보기
def view(request):
    name = request.GET.get('name')
    print("전달이름: ",name)
    qs = Student.objects.get(name=name)
    context = {'stu':qs}
    return  render(request,'students/view.html',context)

# 학생정보 등록
def write(request):
    if request.method == 'POST':  # POST방식으로 들어올 때 - 정보를 DB저장
        name = request.POST.get('name')
        major = request.POST.get('major')
        grade = request.POST.get('grade')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        print("입력된 정보: ",name,major,grade,age,gender)
        ## DB저장
        ## 1. 데이터.save() / 2. create()
        Student(name=name,major=major,grade=grade,age=age,gender=gender).save()
        print("Student 객체 저장")
        return redirect('/students/list/')
    
    else:  # GET방식으로 들어올 때
        print("request method: ",request.method)
        return render(request,'students/write.html')


# 학생정보 리스트
def list(request):
    # DB검색
    # objects.all():전체가져오기
    # objects.get():해당되는것 가져오기
    # objects.filter():검색기능 - __contains, gte, gt, lte, lt
    # objects.order_by(): 정렬, - 역순정렬
    # qs = Student.objects.all()  # 전체가져오기
    qs = Student.objects.order_by("-id") # 순차정렬 -역순정렬
    context = {'list':qs,'count':100,'id':'aaa'}  # 딕셔너리 타입으로 전달
    return render(request,'students/list.html',context)


