from django.urls import path,include
from . import views

# app_name
app_name='students'
urlpatterns = [
    path('list/',views.list, name='list'),
    path('view/',views.view, name='view'),
    path('write/',views.write, name='write'),
    path('delete/',views.delete, name='delete'),
]
