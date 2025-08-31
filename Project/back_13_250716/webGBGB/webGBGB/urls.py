from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('cscenter/', include('cscenter.urls')),
    path('booksearch/', include('booksearch.urls')),
    path('bookmark/', include('bookmark.urls')),
    path('review/', include('review.urls')),
    path('member/', include('member.urls')),
    path('mypage/', include('mypage.urls')),
    path('shareMain/', include('shareMain.urls')),
    path('reply/', include('reply.urls')),
    path('chart/', include('chart.urls')),
    path('chatrooms/', include('chatrooms.urls')),
    path('feedpage/', include('sns_feed.urls')),
    
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)