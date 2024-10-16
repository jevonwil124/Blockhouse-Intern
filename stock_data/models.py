from django.db import models

class StockPrice(models.Model):
    symbol = models.CharField(max_length=10)
    timestamp = models.DateField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('symbol', 'timestamp')
        ordering = ['timestamp']


# Create your models here.
