import requests, json
import uuid

from decouple import config
from celery import shared_task

from payment.serializers import TransferSerializer

from bank.models import Bank


@shared_task
def create_banks():
  endpoint = 'https://api.paystack.co/bank?currency=GHS&type=mobile_money'
  headers = {
    "Authorization": 'Bearer' + config('PAYSTACK_ACCESS_TOKEN')
  }
  try:
    response = requests.get(endpoint, headers=headers)
  except requests.ConnectionError as e:
    raise Exception('Failed operation', e)
  
  if response.status_code in [200,201]:
    data = response.json()
    banks = data.get('data')
    batch = [Bank(
      id= row['id'], 
      name= row['name'],
      slug= row['slug'],
      code= row['code'],
      longcode= row['longcode'],
      gateway=row['gateway'],
      pay_with_bank=row['pay_with_bank'],
      active=row['active'],
      country=row['country'],
      currency=row['currency'],
      type=row['type'],
      is_deleted=row['is_deleted'],
      created_at=row['createdAt'],
      updated_at=row['updatedAt']) for row in banks]
    Bank.objects.bulk_create(batch)
    
@shared_task
def initiate_transfer(data, recipient_id):
  headers = {
    'Authorization': 'Bearer ' + config('PAYSTACK_ACCESS_TOKEN')
  }
  
  endpoint = f'https://api.paystack.co/transfer'
  response = requests.post(endpoint, data=data, headers=headers)
  transfer = response.json()
  if transfer.get('status') == True:
    
    transfer_code = transfer.get('data').get('transfer_code')
    status = transfer.get('data').get('status')
    reason = transfer.get('data').get('reason')
    amount = int(transfer.get('data').get('amount')) / 100
    currency = transfer.get('data').get('currency')
    reference = transfer.get('data').get('reference')
    source = transfer.get('data').get('source')
    
    data = {
      "recipient_id": recipient_id,
      "amount": amount,
      "currency": currency,
      "reference":  reference,
      "transfer_code": transfer_code,
      "status": status,
      "reason": reason,
      "source": source
    }

    serializer = TransferSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return serializer.data
  else:
    return transfer

@shared_task
def initiate_bulk_transfer(data, resp_data):
  headers = {
    'Authorization': 'Bearer ' + config('PAYSTACK_ACCESS_TOKEN')
  }
  endpoint = f'https://api.paystack.co/transfer/bulk'
  response = requests.post(endpoint, data=data, headers=headers)
  transfer = response.json()

  t_data = []
  
  for index, row in enumerate(transfer.get('data')):
    obj = {
      "amount": row['amount'],
      "transfer_code": row['transfer_code'],
      "currency": row['currency'],
      "status": row['status'],
      "recipient_id": resp_data[index].get('recipient_id'),
      "reason": resp_data[index].get('reason'),
      "source": 'balance'
    }
    t_data.append(obj)
  
  serializer = TransferSerializer(data=t_data, many=True)
  serializer.is_valid(raise_exception=True)
  serializer.save()