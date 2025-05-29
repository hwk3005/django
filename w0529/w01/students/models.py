from django.db import models

class Student(models.Model):
    # 번호가 순차적으로 증가
    no = models.AutoField(primary_key=True)  # sequence
    # 문자타입 CharField / 숫자타입 IntegerFiel
    name = models.CharField(max_length=100)  # varchar2
    major = models.CharField(max_length=100)
    grade = models.IntegerField(default=0)  # number
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=30,blank=True)  # 추가-100개
    hobby = models.CharField(max_length=100,blank=True)
    sdate = models.DateTimeField(auto_now=True)  # date - sysdate
    memo = models.TextField(blank=True)     # clob
    
    def __str__(self):
        return f"{self.no},{self.name},{self.sdate}"
