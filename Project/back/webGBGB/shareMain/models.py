from django.db import models

class ReadingGroup(models.Model):
    name = models.CharField(max_length=100)
    member_count = models.IntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}, {self.member_count}, {self.description}'