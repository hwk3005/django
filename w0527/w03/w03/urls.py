from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')), #home등록
    path('students/', include('students.urls')), #students 등록
]
