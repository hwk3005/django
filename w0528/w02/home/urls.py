from django.urls import path, include
from . import views

app_name = ''
urlpatterns = [
    path('', views.index, name='index'),  # index.html페이지 연결
]
