from django.urls import path,include
from . import views

app_name='member'
urlpatterns = [
    path('login/', views.login,name='login'),
    path('logout/', views.logout,name='logout'),
    path('step01/', views.step01,name='step01'),
    path('step02/', views.step02,name='step02'),
    path('emailSend/', views.emailSend,name='emailSend'),
    path('confirmChk/', views.confirmChk,name='confirmChk'),
]
