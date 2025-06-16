from django.urls import path,include
from . import views

app_name = 'board'
urlpatterns = [
    
    # ajax 전송형태
    path('list3/', views.list3, name='list3'),
    path('ajax3/', views.ajax3, name='ajax3'),
    
    # form 파라미터 형태
    path('list/', views.list, name='list'),
    path('view/', views.view, name='view'),
    
    # form url api형태
    path('list2/', views.list2, name='list2'),
    path('view2/<int:bno>/', views.view2, name='view2'),
]
