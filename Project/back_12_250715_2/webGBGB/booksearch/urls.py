from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='booksearch'
urlpatterns = [
    path('search/', views.search, name='search'), # list 페이지 연결
    path('detail/<int:book_id>/', views.detail, name='detail'), # list 페이지 연결
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)