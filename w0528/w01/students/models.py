from django.db import models

# Student 테이블 생성 - name,major,grade,age,gender
class Student(models.Model):
    name = models.CharField(max_length=100) #문자형 타입
    major = models.CharField(max_length=100)
    grade = models.IntegerField(default=0) # 숫자형타입-정수,실수
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.name},{self.major}"
