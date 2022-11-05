from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class CustomUserManager(BaseUserManager):
  def _create_user(self, email, password, **extra_fields):
    if not email:
      raise ValueError('Email field is required.')
    
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save()
    
    return user
    
  def create_superuser(self, email, password, **extra_fields):
    extra_fields.setdefault('is_active', True)
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('name', 'admin')
    
    if extra_fields.get('is_staff') is not True:
      raise ValueError('Superuser user must have is_staff=True.')
    
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True.')
    
    return self._create_user(email, password, **extra_fields)
  
class CustomUser(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(unique=True)
  name = models.CharField(max_length=100)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.email
  
  USERNAME_FIELD = 'email'
  objects = CustomUserManager()
  
  class Meta:
    ordering = ('-created_at',)
    verbose_name_plural = 'CustomUser'
  
class AddressInfo(models.Model):
  country = models.CharField(max_length=50)
  region = models.CharField(max_length=100)
  district = models.CharField(max_length=100)
  city = models.CharField(max_length=100)
  address_line = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"{self.country} - {self.region} - {self.district} - {self.city} - {self.address_line}"
  
  class Meta:
    ordering = ('-created_at',)
    verbose_name_plural = 'AddressInfo'
  
def upload_to(instance, filename):
  return f'profiles/{filename}'

class UserProfile(models.Model):
  user = models.OneToOneField(CustomUser, related_name='user_profile', on_delete=models.CASCADE)
  address_info = models.ForeignKey(AddressInfo, related_name='user_address_info', on_delete=models.CASCADE)
  photo = models.ImageField(upload_to='profiles', blank=True, null=True)
  dob = models.DateField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.user.email
  
  class Meta:
    ordering = ('-created_at',)
    verbose_name_plural = 'UserProfile'
  