from django.contrib import admin
from students.models import Student

# admin관리자페이지 - Student 테이블을 추가
admin.site.register(Student)