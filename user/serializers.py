from rest_framework import serializers

from user.models import AddressInfo, CustomUser, UserProfile

class AddressInfoSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = AddressInfo
    fields = '__all__'
    
class UserProfileSerializer(serializers.ModelSerializer):
  user = serializers.CharField(read_only=True)
  user_id = serializers.IntegerField(write_only=True)
  address_info = AddressInfoSerializer(read_only=True)
  address_info_id = serializers.IntegerField(write_only=True)
  photo = serializers.ImageField(required=False)
  
  class Meta:
    model = UserProfile
    fields = '__all__'
    
class CustomUserSerializer(serializers.ModelSerializer):
  user_profile = UserProfileSerializer(read_only=True)
  
  class Meta:
    model = CustomUser
    fields = ('id', 'email', 'name', 'password', 'user_profile', 'created_at', 'updated_at')
    

