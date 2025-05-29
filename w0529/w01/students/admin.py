from django.contrib import admin
from students.models import Student

# 관리자페이지에 Student테이블 등록
admin.site.register(Student)