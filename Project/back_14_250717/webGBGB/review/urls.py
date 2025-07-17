
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'review'

urlpatterns = [
    path('create/',views.review_create,name='review_create'),
    path('like/',views.review_like,name='review_like'),
    path('update/', views.review_update, name='review_update'),  # ← 추가!
    path('delete/<int:review_id>/',views.review_delete,name='review_delete'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)