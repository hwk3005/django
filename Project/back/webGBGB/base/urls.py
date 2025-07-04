from django.urls import path,include
from . import views

app_name = ''
urlpatterns = [
    path('', views.base, name='base'),
]

# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)