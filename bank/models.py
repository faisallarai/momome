from django.db import models

# Create your models here.
class Bank(models.Model):
  name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(max_length=70, unique=True)
  code = models.CharField(max_length=10, unique=True)
  longcode = models.CharField(max_length=50, blank=True)
  gateway = models.CharField(max_length=50, null=True)
  pay_with_bank = models.BooleanField(default=False)
  active = models.BooleanField(default=True)
  is_deleted = models.BooleanField(max_length=50, null=True)
  country = models.CharField(max_length=50)
  currency = models.CharField(max_length=5)
  type = models.CharField(max_length=15)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.name
  
  class Meta:
    ordering = ('-created_at',)
    verbose_name_plural = 'Banks'
    verbose_name = 'Bank'