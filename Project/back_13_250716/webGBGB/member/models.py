from django.db import models

# Create your models here.
class Member(models.Model):
    member_id = models.AutoField(primary_key=True) # 회원번호
    name = models.CharField(max_length=50)
    id = models.CharField(max_length=50)
    pw = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    gender = models.CharField(max_length=20,blank=True, null=True)
    birth = models.CharField(max_length=100,blank=True, null=True)
    genres = models.CharField(max_length=100,blank=True, null=True)
    
    mdate = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.member_id}, {self.id}, {self.name}'
    