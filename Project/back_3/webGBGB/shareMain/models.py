from django.db import models
from booksearch.models import Book

class ReadingGroup(models.Model):
    group_name = models.CharField(max_length=100)
    max_member = models.IntegerField(default=10)
    description = models.TextField(blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=1)
    tag = models.CharField(max_length=50, blank=True, null=True)
    is_public = models.CharField(max_length=1, choices=[("0", "공개"), ("1", "비공개")], default="0")
    password = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def tags_list(self):
        return self.tag.split(",") if self.tag else []
    
    def __str__(self):
        return f'{self.group_name}'
    

# class GroupMembership(models.Model):
#     group = models.ForeignKey(ReadingGroup, on_delete=models.CASCADE)
#     member = models.ForeignKey(Member, on_delete=models.CASCADE)
#     joined_at = models.DateTimeField(auto_now_add=True)
#     role = models.CharField(max_length=20, default='member')  # 'admin', 'member' 등
#     class Meta:
#         unique_together = ('group', 'member')  # 중복 방지