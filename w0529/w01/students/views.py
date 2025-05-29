from django.shortcuts import render, redirect
from students.models import Student  # Student 테이블 연결

# 학생정보삭제
def delete(request,no):
    Student.objects.get(no=no).delete()
    # return redirect('/students/list/')
    return redirect('students:list')   # app_name, path name

# 학생정보수정페이지 열기
def update(request,no):
    qs = Student.objects.get(no=no)     # set타입 1개
    context = {'stu':qs}
    # 아래와 같이 쓸 수도 있음
    # qs = Student.objects.filter(no=no)  # 데이터 타입 - 리스트타입
    # context = {'stu':qs[0]}
    return render(request,'students/update.html',context)

# 학생정보 수정완료
def updateOk(request):
    no = request.POST.get('no')
    qs = Student.objects.get(no=no)  # 데이터 검색
    # 데이터 수정    
    qs.name = request.POST.get('name')
    qs.major = request.POST.get('major')
    qs.grade = request.POST.get('grade')
    qs.age = request.POST.get('age')
    qs.gender = request.POST.get('gender')
    hobby = request.POST.getlist('hobby')
    hobby = ','.join(hobby)
    qs.hobby = hobby
    qs.save()
    
    return redirect(f'/students/view/{no}/')

# 학생정보 상세보기
def view(request,no):
    try:
        qs = Student.objects.get(no=no)
    except:
        qs = None
    print('전달 no: ',no)
    context = {'stu':qs}
    return render(request,'students/view.html',context)

# 학생정보저장
def writeOk(request):
    # 학생정보저장
    # major = request.POST['major'] 이렇게도 가능
    name = request.POST.get('name')
    major = request.POST.get('major')
    grade = request.POST.get('grade')
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    # 취미 - 리스트
    hobby = request.POST.getlist('hobby')
    # 리스트타입 -> str타입으로 변경
    hobby = ','.join(hobby)  # 'game, golf, swim'
    
    print("저장정보 이름: ",name)
    print("저장정보 학과: ",major)
    print("저장정보 취미: ",hobby)  # ['game','golf','swim']
    
    Student(name=name,major=major,grade=grade,age=age,gender=gender,hobby=hobby,memo='등록합니다.').save()
    
    return redirect('/students/list/')

# 학생정보등록페이지 열기
def write(request):
    return render(request,'students/write.html')

# 학생정보리스트
def list(request):
    qs = Student.objects.all()
    context = {'list':qs}
    
    # render 폴더 앞에  / 안 붙임
    return render(request,'students/list.html',context)
