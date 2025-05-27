from django.urls import path,include
from . import views

app_name = 'students'
urlpatterns = [
    path('list/',views.list,name='list'), # 학생전체리스트
    path('view/',views.view,name='view'), # 학생상세페이지  
    path('write/',views.write,name='write'),   # 학생입력페이지
    path('delete/',views.delete,name='delete'),  # 학생삭제페이지 
]
