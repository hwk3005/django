
from django.urls import path,include
from . import views

app_name = 'bookmark'

urlpatterns = [
    path('create/',views.bookmark_create,name='bookmark_create'),
]