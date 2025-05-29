from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # index연결
    path('member/', include('member.urls')),  # member연결
    path('board/', include('board.urls')),  # board연결
]
