from django.shortcuts import render
from decouple import config

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from transaction.policies import TrannsactionAccessPolicy

from .serializers import TransactionSerializer
from .models import Transaction, Recipient
from .helpers import get_digest

# Create your views here.
class TransactionView(viewsets.ModelViewSet):
  serializer_class = TransactionSerializer
  queryset = Transaction.objects.select_related('recipient')
  permission_classes = (TrannsactionAccessPolicy,)
  
  def create(self, request, *args, **kwargs):
    digest = get_digest(config('PAYSTACK_ACCESS_TOKEN'), request.data)
    
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
      amount = int(request.data.get('data').get('amount')) / 100
      reason = request.data.get('data').get('reason')
      description = request.data.get('data').get('description')
      source = request.data.get('data').get('source')
      reference = request.data.get('data').get('reference')
      status = request.data.get('data').get('status')
      fee_charged = request.data.get('data').get('fee_charged')

      recipient = list(Recipient.objects.filter(recipient_code=recipient_code))
      if recipient:
        recipient_id = recipient[0].id

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
  
  