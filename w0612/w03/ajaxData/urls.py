from django.urls import path,include
from . import views

app_name = 'ajaxData'
urlpatterns = [
    path('bwrite/', views.bwrite, name='bwrite'),
    path('blist/', views.blist, name='blist'),
]
