from django.urls import path, include
from .views import (
    sns_html_view,
    PostListView, PostDetailView, PostLikeView, CommentListView,
    UserProfileUploadView,
    ChatRoomDetailView, ChatRoomJoinView # 리딩그룹 관련 뷰
)

urlpatterns = [
    # html 렌더링뷰
    path('sns_feed/<int:chat_id>/', sns_html_view, name='sns-page'),


    path('reading-groups/<int:reading_group_id>/posts/', PostListView.as_view(), name='post-list-create-by-group'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', PostLikeView.as_view(), name='post-like'),
    path('posts/<int:post_pk>/comments/', CommentListView.as_view(), name='comment-list'),
    path('profile/upload/', UserProfileUploadView.as_view(), name='profile-upload'),


    # --- ReadingGroup 관련 API 경로 ---
    # `ChatRoomDetailView`와 `ChatRoomJoinView`를 ReadingGroup에 맞춰 추가
    path('reading-groups/<int:pk>/', ChatRoomDetailView.as_view(), name='reading-group-detail'),
    path('reading-groups/<int:pk>/join/', ChatRoomJoinView.as_view(), name='reading-group-join'),
]