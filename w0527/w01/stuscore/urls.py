from django.urls import path,include
from . import views

app_name = 'stuscore'
urlpatterns = [
    path('list/', views.list, name='list'), #list url -> list함수호출
]