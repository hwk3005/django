from django.urls import path,include
from . import views

app_name='students'
urlpatterns = [
    path('list/',views.list,name='list'),
]
