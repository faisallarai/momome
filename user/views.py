from django.shortcuts import render
from django.db import transaction

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from user.models import CustomUser

from user.serializers import AddressInfoSerializer, CustomUserSerializer, UserProfileSerializer

# Create your views here.

class CustomUserView(viewsets.ModelViewSet):
  serializer_class = CustomUserSerializer
  queryset = CustomUser.objects.prefetch_related('user_profile')
  # permission_classes = [AllowAny]

  
  def create(self, request, *args, **kwargs):
    with transaction.atomic():
      user_serializer = self.serializer_class(data=request.data)
      user_serializer.is_valid(raise_exception=True)
      user_serializer.save()
      
      address_info_serializer = AddressInfoSerializer(data=request.data)
      address_info_serializer.is_valid(raise_exception=True)
      address_info_serializer.save()

      user_profile_data = {**request.data, "user_id": user_serializer.data['id'], "address_info_id": address_info_serializer.data['id']}
      user_profile_serializer = UserProfileSerializer(data=user_profile_data)
      user_profile_serializer.is_valid(raise_exception=True)
      user_profile_serializer.save()
      
    return Response(self.serializer_class(self.get_queryset().get(id=user_serializer.data['id'])).data, status=201)
      
  def update(self, request, *args, **kwargs):
    instance = self.get_object()
    with transaction.atomic():
      user_serializer = self.serializer_class(data=request.data, instance=instance, partial=True)
      user_serializer.is_valid(raise_exception=True)
      user_serializer.save()
      
      address_info_serializer = AddressInfoSerializer(data=request.data, instance=instance.user_profile.address_info, partial=True)
      address_info_serializer.is_valid(raise_exception=True)
      address_info_serializer.save()

      user_profile_serializer = UserProfileSerializer(data=request.data, instance=instance.user_profile, partial=True)
      user_profile_serializer.is_valid(raise_exception=True)
      user_profile_serializer.save()
      
      return Response(self.serializer_class(self.get_object()).data)