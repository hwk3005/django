from django.shortcuts import render
from students.models import Student



# 학생정보리스트
def list(request):
    qs = Student.objects.all()
    context = {'list':qs}
    return render(request,'students/list.html', context)
