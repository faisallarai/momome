import requests, uuid, json, hmac, hashlib, base64
from decouple import config

from django.shortcuts import render
from django.db import transaction
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status, viewsets, views
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from payment.helpers import create_tranfer_recipient, validate_account_number

from payment.policies import TransferAccessPolicy

from .serializers import TransferSerializer, RecipientSerializer
from .models import Transfer, Recipient
from momome.tasks import initiate_transfer, initiate_bulk_transfer

# Create your views here.

class TransferView(viewsets.ModelViewSet):
  serializer_class = TransferSerializer
  queryset = Transfer.objects.select_related('recipient')
  permission_classes = (TransferAccessPolicy, )
  
  @action(detail=False, methods=['post'])
  def send(self, request, *args, **kwargs):
    name = request.data.get('name', None)
    bank_code = request.data.get('bank_code', None)
    account_number = request.data.get('account_number', None)
    currency = request.data.get('currency', None)
    amount = int(request.data.get('amount', 0)) * 100
    reason = request.data.get('reason', None)
    email = request.data.get('email', None)
    description = request.data.get('description', None)
    type = request.data.get('type', None)
    
    recipient_code = ''
    type = ''
    active = False
    is_deleted = False
    bank_name = ''
    recipient_id = 0
    recipient = list(Recipient.objects.filter(account_number=str(account_number),bank_code=str(bank_code)))
    if not recipient:
      # Verify account number
      account = validate_account_number(bank_code, account_number)

      if account.get('status') is not True:
        return Response(account)
      
      account_name = account.get('data').get('account_name')
      
      # Transfer recipient
      recipient_data = {
        "name": account_name, 
        "account_number": account_number, 
        "bank_code": bank_code, 
        "currency": currency,
        "type": type
      }
    
      recipient = create_tranfer_recipient(recipient_data)
      if recipient.get('status') is not True:
        return Response(recipient)
      
      recipient_code = recipient.get('data').get('recipient_code')
      type = recipient.get('data').get('type')
      active = recipient.get('data').get('active')
      is_deleted = recipient.get('data').get('is_deleted')
      bank_name = recipient.get('data').get('details').get('bank_name')
      
      data = {
        "currency": currency,
        "recipient_code": recipient_code,
        "type": type,
        "active": active,
        "is_deleted": is_deleted,
        "account_number": account_number,
        "name": name,
        "account_name": account_name,
        "bank_code": bank_code,
        "bank_name": bank_name,
        "email": email,
        "description": description
      }
      r_serializer = RecipientSerializer(data=data)
      r_serializer.is_valid(raise_exception=True)
      r_serializer.save()
      recipient_id = r_serializer.data['id']
    else:
      recipient_code = recipient[0].recipient_code
      type = recipient[0].type
      active = recipient[0].active
      is_deleted = recipient[0].is_deleted
      bank_name = recipient[0].bank_name
      recipient_id = recipient[0].id
    
    reference = uuid.uuid4()    
    transfer_data = {
      "amount": amount,
      "reference": reference, 
      "recipient": recipient_code, 
      "reason": reason,
    }
    initiate_transfer.delay(transfer_data, recipient_id)
    
    return Response({'status': True, 'message': 'Transfer queued successfully.', "data": {"reference": reference}}, status=status.HTTP_201_CREATED)
  
  @action(detail=False, methods=['post'])
  def bulk(self, request, *args, **kwargs):
    with transaction.atomic():
      transfer_data =[]
      resp_data = []
      
      for r in request.data:
        name = r.get('name', None)
        bank_code = r.get('bank_code', None)
        account_number = r.get('account_number', None)
        currency = r.get('currency', None)
        amount = r.get('amount', None)
        reason = r.get('reason', None)
        email = r.get('email', None)
        description = r.get('description', None)

        recipient_code = ''
        type = ''
        active = False
        is_deleted = False
        bank_name = ''
        recipient_id = 0
        recipient = list(Recipient.objects.filter(account_number=account_number,bank_code=bank_code))
        
        if not recipient:
          # Verify account number
          account = validate_account_number(bank_code, account_number)
          if account.get('status') is not True:
            return Response(account)
          
          account_name = account.get('data').get('account_name')
          
          # Transfer recipient
          recipient_data = {
            "name": account_name, 
            "account_number": account_number, 
            "bank_code": bank_code, 
            "currency": currency
          }
        
          recipient = create_tranfer_recipient(recipient_data)
          if recipient.get('status') is not True:
            return Response(recipient)
          
          recipient_code = recipient.get('data').get('recipient_code')
          type = recipient.get('data').get('type')
          active = recipient.get('data').get('active')
          is_deleted = recipient.get('data').get('is_deleted')
          bank_name = recipient.get('data').get('details').get('bank_name')
          
          data = {
            "currency": currency,
            "recipient_code": recipient_code,
            "type": type,
            "active": active,
            "is_deleted": is_deleted,
            "account_number": account_number,
            "name": name,
            "account_name": account_name,
            "bank_code": bank_code,
            "bank_name": bank_name,
            "email": email,
            "description": description
          }
          r_serializer = RecipientSerializer(data=data)
          r_serializer.is_valid(raise_exception=True)
          r_serializer.save()
          recipient_id = r_serializer.data['id']
        else:
          recipient_code = recipient[0].recipient_code
          type = recipient[0].type
          active = recipient[0].active
          is_deleted = recipient[0].is_deleted
          bank_name = recipient[0].bank_name
          recipient_id = recipient[0].id
        
        # Transfer
        transfer_data.append({
          "amount": amount,
          "reason": reason,
          "recipient": recipient_code
        })
        resp_data.append({
          "recipient_id": recipient_id,
          "reason": reason
        })
        
      obj = {
          "currency": currency, 
          "source": "balance",
          "transfers": transfer_data
        }
      
      initiate_bulk_transfer.delay(json.dumps(obj), resp_data)
      
    return Response({'status': True, 'message': 'Transfers queued successfully.'}, status=status.HTTP_201_CREATED)
  
class TestExceptionView(views.APIView):
  permission_classes = [AllowAny]
  
  def get(self, request):
    a = 2 / 0
    
    return Response({'ans': [a]})