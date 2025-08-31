from django.db import models
from django.conf import settings
from shareMain.models import ReadingGroup # ReadingGroup 모델 임포트

# class GroupChatRoom(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     max_members = models.IntegerField(default=10)
#     current_members = models.IntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    # group 필드를 GroupChatRoom에서 ReadingGroup으로 변경
    group = models.ForeignKey(ReadingGroup, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # group이 ReadingGroup 인스턴스이므로 group_name 속성 사용
        return f"Post by {self.author.username} in {self.group.group_name}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}"


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Like(models.Model):
    """
    사용자가 게시글에 '좋아요'를 누른 것을 기록하는 모델.
    한 사용자가 한 게시글에 중복으로 좋아요를 누를 수 없도록 unique_together 제약을 설정합니다.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post') # 한 사용자가 한 게시글에 한 번만 좋아요를 누를 수 있도록