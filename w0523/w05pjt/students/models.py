from django.db import models

# ORM : Object Relational Mapping
# class객체 등록하면 db가 자동으로 생성
class Student(models.Model):
    name = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    grade = models.IntegerField(default=0)
    gender = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name+","+self.major



# 오라클 table생성
# create table student (
#     name varchar2(100),
#     major varchar2(100),
#     age number(3),
#     grade number(1),
#     gender varchar2(6)   
# )
