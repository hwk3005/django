from django.urls import path,include
from . import views

app_name='board'
urlpatterns = [
    path('', views.list, name='list' ),        # 게시판리스트
    path('list/', views.list, name='list' ),   # 게시판리스트
    path('write/', views.write, name='write' ),              # 글쓰기 
    path('view/<int:bno>/', views.view, name='view' ),       # 글 상세보기
    path('update/<int:bno>/', views.update, name='update' ), # 글수정
]
