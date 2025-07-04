from django.urls import path,include
from . import views

app_name = 'shareMain'
urlpatterns = [
    path('Share_Main/', views.Share_Main, name='Share_Main'),
    path('Share_AddGroup/', views.Share_AddGroup, name='Share_AddGroup'),

]

# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)