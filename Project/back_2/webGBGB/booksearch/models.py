from django.db import models

# Create your models here.
class Book(models.Model):
    book_id = models.AutoField(primary_key=True) # 기본키 등록
    cover = models.URLField(max_length=1500)  # 표지 이미지 (URL)
    book_url = models.URLField(max_length=1500) # 책 상세 페이지 URL
    title = models.CharField(max_length=1000)  # 제목
    author = models.CharField(max_length=1000)  # 저자 (리스트는 문자열로 저장)
    publisher = models.CharField(max_length=500) # 출판사
    pub_date = models.CharField(max_length=500) # 출판일
    ISBN = models.CharField(max_length=500) # ISBN
    page = models.IntegerField(default=0) # 쪽수
    size = models.CharField(max_length=500, blank=True) # 크기
    review_count = models.IntegerField(default=0) # 리뷰 수
    bookmark_count = models.IntegerField(default=0) # 북마크 수
    rating = models.IntegerField(default=0) # 평점
    views = models.IntegerField(default=0) # 조회수
    
    def __str__(self):
        return f"{self.book_id}, {self.title}, {self.author}"