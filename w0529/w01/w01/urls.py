from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('students/') ## /를 꼭 붙여야 함.
    path('students/', include('students.urls')),  # students
    path('', include('home.urls')),  # home
]
