from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # home
    path('students/', include('students.urls'))  # 학생정보리스트   
]
