from django.db import models
from django.contrib.auth.models import User

# the rate of the transaction
class Rate(models.Model):
    unitRate = models.FloatField(default=None)
    currency_from = models.CharField(max_length=50)
    currency_to = models.CharField(max_length=50, default="Gourdes")
    rate_set = models.DateField(auto_now=True)
    rate_status = models.BooleanField(default=True, null=False)
    rate_description = models.CharField(max_length=200, default=None, null=False)

    #add string method
    def __str__ (self):
        return 'description: %s with rate: %s' % (self.rate_description, self.unitRate)
    
#the transaction of each transfer
class Transaction(models.Model):
    transfer_Date = models.DateField(auto_now=True)
    transfer_origin = models.CharField(max_length=50, default=None, null=False)
    transfer_originAmount = models.FloatField(default=None)
    transfer_givenAmount = models.FloatField(default=None)
    rate = models.FloatField(default=None)
    transfer_comment = models.TextField(null=True)
    transfer_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                    null=False, default=None)
    # add string met
