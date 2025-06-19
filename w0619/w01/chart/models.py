from django.db import models

class TotalSales(models.Model):
    year = models.IntegerField(default=0)
    monthly = models.CharField(max_length=10)
    totalSales = models.IntegerField(default=0)
    profit = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.year},{self.monthly},{self.totalSales},{self.profit}'
