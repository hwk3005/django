from django.db import models
from django.contrib.auth.models import User # 사용자 모델 (선택 사항, 필요에 따라)
from shareMain.models import ReadingGroup
from member.models import Member

# class GroupChatRoom(models.Model):
#     """
#     HTML에 표시되는 채팅방의 상세 정보를 저장하는 모델
#     """
#     # group_id는 Django가 자동으로 id 필드를 생성하므로 명시적으로 추가하지 않아도 됨
#     readingGroup_id = models.ForeignKey(ReadingGroup, on_delete=models.SET_NULL, null=True, blank=True, help_text="채팅방 개설자") # User 모델과 연결
#     # profile_image_url = models.URLField(max_length=500, blank=True, null=True, help_text="채팅방 프로필 이미지 URL") #
    

#     def __str__(self):
#         return self.name

class ChatMessage(models.Model):
    """
    교환독서 그룹 채팅방 DB 이미지에 기반한 채팅 메시지 모델
    """
    # chat_id는 Django가 id 필드를 PK로 자동 생성하므로 명시하지 않음
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, help_text="회원 번호") #
    group_id = models.ForeignKey(ReadingGroup, on_delete=models.CASCADE, help_text="그룹 번호") #
    content = models.TextField(help_text="내용") #
    created_at = models.DateField(auto_now_add=True, help_text="작성일") #
    likes = models.IntegerField(default=0, help_text="좋아요 수") #
    comments = models.IntegerField(default=0, help_text="댓글 수") #
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, help_text="부모 메시지 ID (대댓글용)") #
    file = models.ImageField(upload_to='chat_files/', blank=True, null=True, help_text="이미지") #

    def __str__(self):
        return f"Message by {self.member_id.username} in {self.group_id.name}"