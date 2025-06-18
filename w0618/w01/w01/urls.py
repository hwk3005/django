from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('member/', include('member.urls')),
    path('chart/', include('chart.urls')),
    path('pboard/', include('pboard.urls')),
    path('pboard2/', include('pboard2.urls')),
    path('pboard3/', include('pboard3.urls')),
    path('kakao/', include('kakao.urls')),
]
