from django.db import models

# Create your models here.

class Recipient(models.Model):
  currency = models.CharField(max_length=5, default='GHS')
  recipient_code = models.CharField(max_length=50, unique=True, blank=True)
  type = models.CharField(max_length=50, blank=True)
  active = models.BooleanField(default=False)
  is_deleted = models.BooleanField(default=False)
  account_number = models.CharField(max_length=50)
  name = models.CharField(max_length=50)
  account_name = models.CharField(max_length=50)
  bank_code = models.CharField(max_length=10)
  bank_name = models.CharField(max_length=25, blank=True)
  email = models.EmailField(blank=True)
  description = models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.recipient_code
  
  class Meta:
    ordering = ('-created_at',)
    verbose_name = 'Recipient'
    verbose_name_plural = 'Recipients'
    
class Transfer(models.Model):
  recipient = models.ForeignKey(Recipient, related_name='transfer_recipient', on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
  transfer_code = models.CharField(max_length=50, unique=True)
  currency = models.CharField(max_length=5, default='GHS')
  reason = models.TextField(blank=True)
  reference = models.UUIDField(max_length=50, unique=True, blank=True)
  status = models.CharField(max_length=15, blank=True)
  source = models.CharField(max_length=15, blank=True, default='balance')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.transfer_code
  
  class Meta:
    ordering = ('-created_at',)
    verbose_name = 'Transfer'
    verbose_name_plural = 'Transfers'
    
    
class Transaction(models.Model):
  recipient = models.ForeignKey(Recipient, related_name='transaction_recipient', on_delete=models.SET_NULL, null=True, blank=True)
  recipient_code = models.CharField(max_length=50, blank=True, null=True)
  name = models.CharField(max_length=50, blank=True, null=True)
  bank_code = models.CharField(max_length=50, blank=True, null=True)
  bank_name = models.CharField(max_length=50, blank=True, null=True)
  account_name = models.CharField(max_length=50, blank=True, null=True)
  account_number = models.CharField(max_length=50, blank=True, null=True)
  currency = models.CharField(max_length=5, default='GHS')
  email = models.EmailField(max_length=50, blank=True, null=True)
  type = models.CharField(max_length=50, blank=True, null=True)
  active = models.BooleanField(default=False)
  is_deleted = models.BooleanField(default=False)
  transfer = models.ForeignKey(Transfer, related_name='transaction_transfer', on_delete=models.SET_NULL, null=True, blank=True)
  transfer_code = models.CharField(max_length=50, blank=True, null=True)
  transferred_at = models.DateTimeField(blank=True, null=True)
  amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
  reason = models.TextField(blank=True)
  description = models.CharField(max_length=15, blank=True, null=True)
  source = models.CharField(max_length=15, blank=True, null=True)
  reference = models.UUIDField(max_length=50, blank=True, null=True)
  status = models.CharField(max_length=15, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  
  def __str__(self):
    return f"{self.recipient_code} - {self.transfer_code}"
  
  class Meta:
    ordering = ('-created_at',)
    verbose_name = 'Transaction'
    verbose_name_plural = 'Transactions'