from django.urls import path,include
from . import views

app_name = 'students'
urlpatterns = [
    path('list/', views.list, name='list'), #list url -> list함수호출
    path('write/', views.write, name='write'), # 학생등록페이지
    path('write2/', views.write2, name='write2'), # 학생등록저장
]