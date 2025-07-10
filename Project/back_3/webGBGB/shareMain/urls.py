from django.urls import path,include
from . import views

app_name = 'shareMain'
urlpatterns = [
    path('Share_Main/', views.Share_Main, name='Share_Main'),
    path('Share_AddGroup/', views.Share_AddGroup, name='Share_AddGroup'),
    path("shareMain/ajax_search/", views.ajax_search, name="ajax_search"),
]
