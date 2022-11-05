from django.shortcuts import render

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import BankSerializer
from .models import Bank
from momome.tasks import create_banks

# Create your views here.
class BankView(viewsets.ModelViewSet):
  serializer_class = BankSerializer
  queryset = Bank.objects.all()
  
  def create(self, request, *args, **kwargs):
    print(Bank.objects.count())
    if Bank.objects.count() == 0:
      create_banks.delay()
    serializer = self.serializer_class(self.queryset, many=True)
    return Response({'message': 'Banks created successfully.', 'data': serializer.data})

