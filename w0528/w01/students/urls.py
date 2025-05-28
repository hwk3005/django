from django.urls import path, include
from . import views

app_name = 'students'
urlpatterns = [
    path('list/', views.list, name='list'),  # list.html 페이지 연결
    path('write/', views.write, name='write'),  # write.html - GET, POST
    path('view/', views.view, name='view'),  # view.html
    path('update/<str:name>/', views.update, name='update'),  # update.html
    path('delete/<str:name>/', views.delete, name='delete'),  # delete.html
]
