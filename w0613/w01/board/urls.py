from django.urls import path,include
from . import views

app_name = 'board'
urlpatterns = [
    path('list/', views.list, name='list'),
    path('view/<int:bno>/', views.view, name='view'),
    
]
