from django.urls import path,include
from . import views

app_name='chart/'
urlpatterns = [
    path('chlist/', views.chlist, name='chlist'),
   
]
