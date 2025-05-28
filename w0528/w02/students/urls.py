from django.urls import path, include
from . import views

app_name = 'students'
urlpatterns = [
    path('list/', views.list, name='list'),  # list.html페이지 연결
    path('write/', views.write, name='write'),  # write.html페이지 연결
    # path('update/', views.update, name='update'),  # update.html페이지 연결
]
