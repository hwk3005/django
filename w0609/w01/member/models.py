from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=50)
    id = models.CharField(max_length=50,primary_key=True)
    pw = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    emailc = models.IntegerField(default=0)
    address1 = models.CharField(max_length=300)
    address2 = models.CharField(max_length=300)
    phone = models.CharField(max_length=50,default='010-0000-0000')
    tel = models.CharField(max_length=50,default='02-0000-0000')
    birth = models.CharField(max_length=20)
    corporate = models.IntegerField(default=0)
    gender = models.CharField(max_length=10,default='남자')
    hobby = models.CharField(max_length=50,default='게임')
    mdate = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.id}, {self.name}'

