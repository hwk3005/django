from django.db import models
from member.models import Member

class Customer(models.Model):
    bno = models.AutoField(primary_key=True) #기본키 등록
    # 외래키(Foreign Key)
    member = models.ForeignKey(Member,on_delete=models.SET_NULL,null=True) # 회원탈퇴시 Null처리
    # member = models.ForeignKey(Member,on_delete=models.CASCADE) # 회원탈퇴시 모두삭제
    # id = models.CharField(max_length=100)    #작성자
    btitle = models.CharField(max_length=1000) #제목
    bcontent = models.TextField()              #내용
    # 답글달기
    bgroup = models.IntegerField(default=0)    #답글달기 묶음
    bstep = models.IntegerField(default=0)     #답글달기 순서
    bindent = models.IntegerField(default=0)   #들여쓰기
    # -----
    bhit = models.IntegerField(default=0)      #조회수
    bfile = models.ImageField(null=True,blank=True,upload_to='customer')
    bfile2 = models.ImageField(null=True,blank=True,upload_to='customer')
    # FileField : 모든파일 업로드 가능
    ntchk = models.IntegerField(default=0)
    bdate = models.DateTimeField(auto_now=True) # 현재날짜시간자동등록
    
    def __str__(self):
        return f'{self.bno},{self.btitle},{self.bgroup}'
    
# class customerFile(models.Model):
#     fno = models.AutoField(primary_key=True) #기본키 등록
#     customer = models.ForeignKey(Customer,on_delete=models.CASCADE) # 회원탈퇴시 모두삭제
#     ffile = models.ImageField(null=True,blank=True,upload_to='board')
#     fdate = bdate = models.DateTimeField(auto_now=True) # 현재날짜시간자동등록
        

