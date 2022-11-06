import requests, uuid, json, hmac, hashlib, base64
from decouple import config

from django.shortcuts import render
from django.db import transaction
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status, viewsets, views
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from payment.helpers import create_tranfer_recipient, get_digest, validate_account_number

from payment.policies import TransferAccessPolicy

from .serializers import TransferSerializer, RecipientSerializer, TransactionSerializer
from .models import Transfer, Recipient
from momome.tasks import initiate_tranfer, initiate_bulk_tranfer

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
    amount = request.data.get('amount', None)
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
        print('rein', account)
        return Response(account)
      
      account_name = account.get('data').get('account_name')
      
      print('acn', account_name)
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
    initiate_tranfer.delay(transfer_data, recipient_id)
    
    return Response({'message': 'Transfer queued successfully.', "data": {"reference": reference}}, status=status.HTTP_201_CREATED)
  
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
      
      initiate_bulk_tranfer.delay(json.dumps(obj), resp_data)
      
    return Response({'message': 'Transfers queued successfully.'}, status=status.HTTP_201_CREATED)
  
  @action(detail=False, methods=['post'], permission_classes=[AllowAny])
  def transaction(self, request, *args, **kwargs):
    print('webhook', request.data)
    digest = get_digest(config('PAYSTACK_ACCESS_TOKEN'), request.data)
    
    # print('digest',digest)
    # print('signature', request.headers.get("x-paystack-signature",None))
    if digest == request.headers.get("x-paystack-signature",None):
      # Recipient
      recipient_code = request.data.get('data').get('recipient').get('recipient_code')
      recipient_id = None
      name = request.data.get('data').get('recipient').get('name')
      bank_code = request.data.get('data').get('recipient').get('details').get('bank_code')
      bank_name = request.data.get('data').get('recipient').get('details').get('bank_name')
      account_name = request.data.get('data').get('recipient').get('details').get('account_name')
      account_number = request.data.get('data').get('recipient').get('details').get('account_number')
      currency = request.data.get('data').get('recipient').get('currency')
      email = request.data.get('data').get('recipient').get('email')
      is_deleted = request.data.get('data').get('recipient').get('is_deleted')
      active = request.data.get('data').get('recipient').get('active')
      type = request.data.get('data').get('recipient').get('type')
      
      # Transfer
      transfer_code = request.data.get('data').get('transfer_code')
      transferred_at = request.data.get('data').get('transferred_at')
      amount = request.data.get('data').get('amount')
      reason = request.data.get('data').get('reason')
      description = request.data.get('data').get('description')
      source = request.data.get('data').get('source')
      reference = request.data.get('data').get('reference')
      status = request.data.get('data').get('status')
      fee_charged = request.data.get('data').get('fee_charged')

      recipient = list(Recipient.objects.filter(recipient_code=recipient_code))
      if recipient:
        recipient_id = recipient[0].id
        
      # print('recipient_code', recipient_code)
      # print('recipient_id', recipient_id)
      # print('name', name)
      # print('bank_code', bank_code)
      # print('bank_name', bank_name)
      # print('account_name', account_name)
      # print('account_number', account_number)
      # print('currency', currency)
      # print('email', email)
      # print('is_deleted', is_deleted)
      # print('active', active)
      # print('type', type)
      # print('transfer_code', transfer_code)
      # print('transferred_at', transferred_at)
      # print('amount', amount)
      # print('reason', reason)
      # print('description', description)
      # print('source', source)
      # print('reference', reference)
      # print('status', status)
      # print('fee_charged', fee_charged)

      trx_obj = {
        'recipient_code': recipient_code,
        'recipient_id': recipient_id,
        'name': name,
        'bank_code': bank_code,
        'bank_name': bank_name,
        'account_name': account_name,
        'account_number': account_number,
        'currency': currency,
        'email': email,
        'is_deleted': is_deleted,
        'active': active,
        'type': type,
        'transfer_code': transfer_code,
        'transferred_at': transferred_at,
        'amount': amount,
        'reason': reason,
        'description': description,
        'source': source,
        'reference': reference,
        'status': status,
        'fee_charged': fee_charged
      }
      
      serializer = TransactionSerializer(data=trx_obj)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      
    return Response(status=200)
  
class TestExceptionView(views.APIView):
  permission_classes = [AllowAny]
  
  def get(self, request):
    a = 2 / 0
    
    return Response({'ans': [a]})