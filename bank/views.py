import requests
from decouple import config

from django.shortcuts import render
from django.core.cache import cache

from rest_framework import status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import BankSerializer
from .models import Bank
from momome.tasks import create_banks

# Create your views here.
def fetch_banks():
  
  try:
    key = f"bank?currency=GHS&type=mobile_money"
    endpoint = 'https://api.paystack.co/bank?currency=GHS&type=mobile_money'
    headers = {
      "Authorization": 'Bearer' + config('PAYSTACK_ACCESS_TOKEN')
    }
    value = cache.get(key)
    if value == None:
      response = requests.get(endpoint, headers=headers)
      cache.set(key, response.json())
      return response.json()
    else:
      return value
  except requests.ConnectionError as e:
    raise Exception('Failed operation', e)
  
class BankView(viewsets.ModelViewSet):
  serializer_class = BankSerializer
  queryset = Bank.objects.all()
  permission_classes = [permissions.AllowAny]
  permission_classes_by_action = {
    'create': [permissions.IsAdminUser],
    'list': [permissions.AllowAny],
    'retrieve': [permissions.AllowAny]
  }
  
  def create(self, request, *args, **kwargs):
    print(Bank.objects.count())
    if Bank.objects.count() == 0:
      create_banks.delay()
    serializer = self.serializer_class(self.queryset, many=True)
    return Response({'message': 'Banks created successfully.', 'data': serializer.data})
  
  def list(self, request, *args, **kwargs):
    bank_obj = fetch_banks()
    if Bank.objects.count() == 0:
      bank_list = bank_obj.get('data')
      serializer = self.serializer_class(data=bank_list, many=True)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response({
        "status": True,
        "message": "Banks retrieved",
        "data": serializer.data
      })
    else:
      return Response(bank_obj)

