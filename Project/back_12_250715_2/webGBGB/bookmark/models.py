from django.db import models
from booksearch.models import Book
from member.models import Member
# Create your models here.
class Bookmark(models.Model):
    bookmark_id = models.AutoField(primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    marked_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bookmark_id}, {self.marked_date}"