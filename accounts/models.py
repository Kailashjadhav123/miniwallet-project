from django.db import models
from django.contrib.auth.models import User



class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return self.user.first_name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return (self.user.username) +" "+ str(self.timestamp)[:16]
    
    def save(self, *args, **kwargs):
        if self.transaction_type.lower() == "deposit":
            wallet = Wallet.objects.get(user=self.user)
            wallet.balance += self.amount
            wallet.save()
            super(Transaction, self).save(*args, **kwargs)
        elif self.transaction_type.lower() == "withdraw":
            wallet = Wallet.objects.get(user=self.user)
            wallet.balance -= self.amount
            wallet.save()
            super(Transaction, self).save(*args, **kwargs)