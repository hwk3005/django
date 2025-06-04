from django.urls import path,include
from . import views

app_name = 'board'
urlpatterns = [
    path('list/', views.list, name='list'),                 #게시판리스트
    path('view/<int:bno>/', views.view, name='view'),       #게시글보기
    path('write/', views.write, name='write'),              #글쓰기
    path('update/<int:bno>/', views.update, name='update'), #수정
    path('delete/<int:bno>/', views.delete, name='delete'), #삭제
    path('reply/<int:bno>/', views.reply, name='reply'),    #답글달기
]