from django.db import models

class Mainbanner(models.Model):
    mno = models.AutoField(primary_key=True)
    mtitle = models.CharField(max_length=100)
    mtitle2 = models.CharField(max_length=100)
    msubtitle = models.CharField(max_length=100)
    msubtitle2 = models.CharField(max_length=100)
    mimg = models.ImageField(upload_to='mainBanner')
    primary = models.IntegerField(default=0)
    mdate = models.DateTimeField(auto_now=True)
    murl = models.CharField(max_length=1000,default='#')
    
    def __str__(self):
        return f'{self.mno}, {self.mtitle}'