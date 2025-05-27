from django.contrib import admin
from students.models import Student

# 관리자페이지에서 컬럼부분 추가해서 보여줌.
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name','major','age']

# 어드민 관리자 페이지 등록
admin.site.register(Student,StudentAdmin)