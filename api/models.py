from django.db import models

# Create your models here.


class Tick(models.Model):
    high = models.DecimalField(max_digits=22, decimal_places=12)
    low = models.DecimalField(max_digits=22, decimal_places=12)
    volume = models.DecimalField(max_digits=22, decimal_places=12)
    bid = models.DecimalField(max_digits=22, decimal_places=12)
    ask = models.DecimalField(max_digits=22, decimal_places=12)
    date = models.DateTimeField(auto_now_add=True)
    currency1 = models.CharField(max_length=5)
    currency2 = models.CharField(max_length=5)

    def __unicode__(self):
        return "<Tick high:%s low:%s volume:%s bid:%s ask:%s time:%s>" % (self.high, self.low, self.volume, self.bid, self.ask, self.date)


class OrderBook(models.Model):
    is_bid = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=22, decimal_places=12)
    price = models.DecimalField(max_digits=22, decimal_places=12)
    currency1 = models.CharField(max_length=5)
    currency2 = models.CharField(max_length=5)
