from django.db import models

class ReadingGroup(models.Model):
    group_name = models.CharField(max_length=100)
    member_count = models.IntegerField(default=2)
    description = models.TextField(blank=True)
    book = models.CharField(max_length=50)
    tag = models.CharField(max_length=50)
    is_public = models.IntegerField(default=0)
    password = models.CharField(max_length=50)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.group_name}, {self.member_count}, {self.description}'