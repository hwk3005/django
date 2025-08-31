from django.urls import path
from . import views

urlpatterns = [
    path('detail/<int:chat_id>/', views.chatroom_detail, name='chatroom-detail'),
    # path('join/',views.chatroom_join, name='chatroom-join'),
    # path('profile/upload/', ProfileUploadView.as_view(), name='profile-upload'),
    
#     path('chatroom/<int:pk>/', ChatRoomDetailView.as_view(), name='chatroom-detail'),
#     path('chatroom/<int:pk>/join/', ChatRoomJoinView.as_view(), name='chatroom-join'),
#     path('profile/upload/', ProfileUploadView.as_view(), name='profile-upload'),
]