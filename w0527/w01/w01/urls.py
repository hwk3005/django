from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')), # home app > urls.py
    path('students/', include('students.urls')), # students app > urls.py
    path('event/', include('event.urls')), # students app > urls.py
    path('stuscore/', include('stuscore.urls')), # students app > urls.py
]
