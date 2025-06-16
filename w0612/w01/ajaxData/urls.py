from django.urls import path,include
from . import views

app_name = 'ajaxData'
urlpatterns = [
    path('blist/', views.blist, name='blist'),
    path('bwrite/', views.bwrite, name='bwrite'),
    path('bdelete/', views.bdelete, name='bdelete'),
    
]
