from django.contrib import admin
from students.models import Student

# admin 관리자페이지 - Student테이블 추가
admin.site.register(Student)