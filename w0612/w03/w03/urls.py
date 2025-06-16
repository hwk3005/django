from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('board/', include('board.urls')),
    path('ajaxData/', include('ajaxData.urls')),
]

# 파일업로드시 url구성 , urlpatterns 에 추가로 설정이 들어감.
urlpatterns += static(settings.MEDIA_URL, 
                      document_root=settings.MEDIA_ROOT)
