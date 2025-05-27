from django.contrib import admin
from students.models import Student

# admin페이지에서 추가적인 컬럼을 보여줌.
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name','major','grade']

admin.site.register(Student,StudentAdmin)
