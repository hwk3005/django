from django.urls import path,include
from . import views

app_name='member/'
urlpatterns = [
    path('step01/', views.step01, name='step01'),
    path('step02/', views.step02, name='step02'),
    path('step03/', views.step03, name='step03'),
    path('step04/', views.step04, name='step04'),
    path('idchk/', views.idchk, name='idchk'),
]
