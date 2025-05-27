from django.urls import path,include
from . import views

app_name = 'students'
urlpatterns = [
    path('list/', views.list,name='list'),
    path('write/', views.write,name='write'),  # 페이지 열기
    path('result/', views.result,name='result'),  # 결과확인
]
