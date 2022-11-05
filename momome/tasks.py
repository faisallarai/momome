import requests

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
    print(banks)
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
    
    
def initiate_tranfer(data):
  headers = {
    'Authorization': 'Bearer ' + config('PAYSTACK_ACCESS_TOKEN')
  }
  endpoint = f'https://api.paystack.co/transfer'
  response = requests.post(endpoint, data=data, headers=headers)
  transfer = response.json()

  # status = transfer.get('data').get('status')
  # if status != 'success':
  #   return Response(transfer)
  
  # transfer_code = transfer.get('data').get('transfer_code')
  # status = transfer.get('data').get('status')
  # reason = transfer.get('data').get('reason')
  
  # print(transfer_code)
  # data = {
  #   "amount": amount,
  #   "currency": currency,
  #   "reference":  reference,
  #   "recipient_id": recipient_id,
  #   "transfer_code": transfer_code,
  #   "status": status,
  #   "reference": reference,
  #   "source": 'balance'
  # }
  
  serializer = TransferSerializer(data=data)
  serializer.is_valid(raise_exception=True)
  serializer.save()

def initiate_bulk_tranfer(data):
  headers = {
    'Authorization': 'Bearer ' + config('PAYSTACK_ACCESS_TOKEN')
  }
  endpoint = f'https://api.paystack.co/transfer/bulk'
  response = requests.post(endpoint, data=data, headers=headers)
  return response.json()