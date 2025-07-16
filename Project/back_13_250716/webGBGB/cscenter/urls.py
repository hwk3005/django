from django.urls import path,include
from . import views

app_name = 'cscenter'

urlpatterns = [
    path('list/', views.list,name='list'),
    path('view/<int:ntcno>/', views.view,name='view'),
    path('inquiry/', views.inquiry,name='inquiry'),
    path('submit/', views.submit,name='submit'),
]