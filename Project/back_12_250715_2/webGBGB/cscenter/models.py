from django.db import models
from member.models import Member

class Notice(models.Model):
    ntcno = models.AutoField(primary_key=True)  # 기본키 등록
    id = models.CharField(max_length=100)     # 작성자
    ntitle = models.CharField(max_length=1000) # 제목
    ncontent = models.TextField()              # 내용

    nfile = models.ImageField(null=True,blank=True,upload_to='notice')
    # FileField : 모든파일 업로드 가능
    nhit = models.IntegerField(default=0)      # 조회수
    ndate = models.DateTimeField(auto_now=True)  # 현재날짜시간자동등록
    
    def __str__(self):
        return f'{self.ntcno},{self.ntitle}'


class Inquiry(models.Model):
    inqno = models.AutoField(primary_key=True)  # 기본키 등록
    # id = models.CharField(max_length=100)     # 작성자
    member = models.ForeignKey(Member, on_delete=models.CASCADE,default=1)
    ictgr = models.CharField(max_length=100)  # 카테고리
    ititle = models.CharField(max_length=1000) # 제목
    icontent = models.TextField()              # 내용
    ifile1 = models.ImageField(null=True,blank=True,upload_to='inquiry')
    ifile2 = models.ImageField(null=True,blank=True,upload_to='inquiry')
    ifile3 = models.ImageField(null=True,blank=True,upload_to='inquiry')
    idate = models.DateTimeField(auto_now=True)  # 현재날짜시간자동등록
    
    def __str__(self):
        return f'{self.inqno},{self.ictgr},{self.ititle}'