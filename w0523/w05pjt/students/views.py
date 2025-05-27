from django.shortcuts import render
# db접근하기 위해 import
from students.models import Student

### 학생리스트 페이지
def list(request):
    ## 데이터 모두 가져오기
    qs = Student.objects.all()
    context = {'list':qs}
    print(qs)
    ### html페이지 연결
    return render(request,'list.html',context)

### 학생상세 페이지
def view(request):
    name = '유관순'
    qs = Student.objects.get(name=name)
    context = {'stu':qs}
    print(qs)
    return render(request,'view.html',context)

