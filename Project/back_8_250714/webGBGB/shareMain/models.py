from django.db import models
from booksearch.models import Book
from member.models import Member

class ReadingGroup(models.Model):
    group_name = models.CharField(max_length=100) # 그룹명
    max_member = models.IntegerField(default=10)  # 최대 참여인원수
    admin = models.ForeignKey(Member, on_delete=models.CASCADE,related_name='admin_reading_groups')  # 세션아이디 로그인중인 유저로 방장 설정
    member = models.ManyToManyField(Member,related_name='member_reading_groups',blank=True)  # 방장 제외 나머지 멤버가 들어옴, null이어도 ok
    description = models.TextField(blank=True)  # 그룹소개글
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=1)  # book모델 연결
    tag = models.CharField(max_length=50, blank=True, null=True)  # 해시태그
    is_public = models.CharField(max_length=1, choices=[("0", "공개"), ("1", "비공개")], default="0")  # 공개여부
    password = models.CharField(max_length=100, blank=True, null=True)  # 그룹 비밀번호
    created_at = models.DateTimeField(auto_now_add=True)  # 만든 날짜

    @property
    def tags_list(self):
        if self.tag:
            return [t for t in self.tag.split("#") if t]
        return []
    
    def __str__(self):
        return f'{self.group_name}'
    

# class GroupMembership(models.Model):
#     group = models.ForeignKey(ReadingGroup, on_delete=models.CASCADE)
#     member = models.ForeignKey(Member, on_delete=models.CASCADE)
#     joined_at = models.DateTimeField(auto_now_add=True)
#     role = models.CharField(max_length=20, default='member')  # 'admin', 'member' 등
#     class Meta:
#         unique_together = ('group', 'member')  # 중복 방지