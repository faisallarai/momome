from django.db import models

# Create your models here.

class Recipient(models.Model):
  currency = models.CharField(max_length=5, default='GHS')
  recipient_code = models.CharField(max_length=50, blank=True, null=True)
  type = models.CharField(max_length=50, default='mobile_money', blank=True, null=True)
  active = models.BooleanField(default=False)
  is_deleted = models.BooleanField(default=False)
  account_number = models.CharField(max_length=50, blank=True, null=True)
  name = models.CharField(max_length=50, blank=True, null=True)
  account_name = models.CharField(max_length=50, blank=True, null=True)
  bank_code = models.CharField(max_length=10, blank=True, null=True)
  bank_name = models.CharField(max_length=25, blank=True, null=True)
  email = models.EmailField(blank=True, null=True)
  description = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.recipient_code
  
  class Meta:
    ordering = ('-created_at',)
    verbose_name = 'Recipient'
    verbose_name_plural = 'Recipients'
    
class Transfer(models.Model):
  recipient = models.ForeignKey(Recipient, related_name='transfer_recipient', on_delete=models.SET_NULL, blank=True, null=True)
  amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  transfer_code = models.CharField(max_length=50, blank=True, null=True)
  currency = models.CharField(max_length=5, default='GHS')
  reason = models.TextField(blank=True, null=True)
  reference = models.UUIDField(max_length=50, blank=True, null=True)
  status = models.CharField(max_length=15, blank=True, null=True)
  source = models.CharField(max_length=15, default='balance')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.transfer_code
  
  class Meta:
    ordering = ('-created_at',)
    verbose_name = 'Transfer'
    verbose_name_plural = 'Transfers'
