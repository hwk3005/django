from django.urls import path,include
from . import views

app_name='kakaomap'
urlpatterns = [
    path('list/', views.list, name='list'),
    path('list2/', views.list2, name='list2'),
]
