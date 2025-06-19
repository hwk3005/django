from django.urls import path,include
from . import views

app_name='pboard2'
urlpatterns = [
    path('list/', views.list, name='list'),
    path('view/<int:galContentId>/', views.view, name='view'),
   
]
