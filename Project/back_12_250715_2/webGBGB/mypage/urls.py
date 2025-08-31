from django.urls import path,include
from . import views

app_name='mypage'

urlpatterns = [
    path('review/', views.review,name='review'),
    path('Bmark/', views.Bmark,name='Bmark'),
    path('mygroup/', views.mygroup,name='mygroup'),
    path('review_delete/', views.review_delete,name='review_delete'),
    path('bookmark_delete/', views.bookmark_delete,name='bookmark_delete'),
    path('mygroup_delete/', views.mygroup_delete,name='mygroup_delete'),
    path('member_delete/', views.member_delete,name='member_delete'),
]

# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)