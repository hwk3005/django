from django.db import models
from customer.models import Customer
from member.models import Member

class Comment(models.Model):
    cno = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE) #게시글삭제시 하단댓글모두삭제
    member = models.ForeignKey(Member,on_delete=models.DO_NOTHING) # 그대로
    cpw = models.CharField(max_length=20,null=True,blank=True)
    ccontent = models.TextField(blank=True)
    cdate = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.cno},{self.member.id},{self.ccontent}'
    
