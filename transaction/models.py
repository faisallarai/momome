from django.db import models
from payment.models import Recipient

# Create your models here.
    
class Transaction(models.Model):
  recipient = models.ForeignKey(Recipient, related_name='transaction_recipient', on_delete=models.SET_NULL, null=True, blank=True)
  recipient_code = models.CharField(max_length=50, blank=True, null=True)
  name = models.CharField(max_length=50, blank=True, null=True)
  bank_code = models.CharField(max_length=50, blank=True, null=True)
  bank_name = models.CharField(max_length=50, blank=True, null=True)
  account_name = models.CharField(max_length=50, blank=True, null=True)
  account_number = models.CharField(max_length=50, blank=True, null=True)
  currency = models.CharField(max_length=5, blank=True, null=True)
  email = models.EmailField(max_length=50, blank=True, null=True)
  type = models.CharField(max_length=50, blank=True, null=True)
  active = models.BooleanField(blank=True, null=True, default=False)
  is_deleted = models.BooleanField(blank=True, null=True, default=False)
  transfer_code = models.CharField(max_length=50, blank=True, null=True)
  transferred_at = models.DateTimeField(blank=True, null=True)
  amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
  reason = models.TextField(blank=True, null=True)
  description = models.CharField(max_length=15, blank=True, null=True)
  source = models.CharField(max_length=15, blank=True, null=True)
  reference = models.CharField(max_length=50, blank=True, null=True)
  status = models.CharField(max_length=15, blank=True, null=True)
  fee_charged = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  
  def __str__(self):
    return f"{self.recipient_code} - {self.transfer_code}"
  
  class Meta:
    ordering = ('-created_at',)
    verbose_name = 'Transaction'
    verbose_name_plural = 'Transactions'