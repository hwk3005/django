from django.urls import path,include
from . import views

app_name=''
urlpatterns = [
    # views.py로 연결
    path('',views.index,name='index'),
]