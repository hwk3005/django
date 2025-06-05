from django.db import models

class Board(models.Model):
    bno = models.AutoField(primary_key=True)
    id = models.CharField(max_length=50)
    btitle = models.CharField(max_length=1000)
    bcontent = models.TextField()
    # 계층형게시판 생성시 필요
    bgroup = models.IntegerField(default=0)
    bstep = models.IntegerField(default=0)
    bindent = models.IntegerField(default=0)
    bhit = models.IntegerField(default=0)
    bfile = models.ImageField(null=True,blank=True,upload_to='board')
    bdate = models.DateField(auto_now=True)
    
    def __str__(self):
        return f'{self.bno}, {self.id}, {self.btitle}'
    
