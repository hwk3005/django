from django.shortcuts import render,redirect
from students.models import Student


# 3. 

# 2. 학생등록 write
def write(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        major = request.POST.get('major')
        grade = request.POST.get('grade')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        print("입력된 정보: ",name,major,grade,age,gender)
        Student(name=name,major=major,grade=grade,age=age,gender=gender)
        print("Student 객체 저장")
        return redirect('/students/list/')
    else:
        print("request method: ",request.method)
        return render(request,'students/write.html')

# 1. 학생정보 리스트 list
def list(request):
    qs = Student.objects.order_by("-major")
    context = {'list':qs,'count':100,'id':'aaa'}
    return render(request,'students/list.html')