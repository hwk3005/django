
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'reply'

urlpatterns = [
    path('create/',views.reply_create,name='reply_create'),
    path('modify/<int:reply_id>/',views.reply_modify,name='reply_modify'),
    path('delete/<int:reply_id>/',views.reply_delete,name='reply_delete'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)