from django.urls import path,include
from . import views

app_name='chart/'
urlpatterns = [
    path('chlist/', views.chlist, name='chlist'),
    path('chlist2/', views.chlist2, name='chlist2'),
    path('chajax/', views.chajax, name='chajax'),
   
]
