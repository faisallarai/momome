import json, hmac, hashlib, requests
from decouple import config

from django.core.cache import cache

def get_digest(key, data):
  secret = bytes(key.encode('utf8'))
  data = json.dumps(dict(data), separators=(',', ':')).encode('utf8')
  hash = hmac.new(key=secret, digestmod=hashlib.sha512)
  hash.update(data)
  digest = hash.hexdigest()
  return digest


def validate_account_number(bank_code, account_number):
  key = f"bank/resolve?account_number={account_number}&bank_code={bank_code}"
  value = cache.get(key)
  if value == None:
    headers = {
      'Authorization': 'Bearer ' + config('PAYSTACK_ACCESS_TOKEN')
    }
    endpoint = f'https://api.paystack.co/bank/resolve?account_number={account_number}&bank_code={bank_code}'
    response = requests.get(endpoint, headers=headers)
    cache.set(key, response.json())
    return response.json()
  else:
    return value

def create_tranfer_recipient(data):
  name = data.get('name')
  account_number = data.get('account_number')
  bank_code = data.get('bank_code')
  currency = data.get('currency')

  key = f"transferrecipient/{name}/{account_number}/{bank_code}/{currency}"
  value = cache.get(key)
  if value == None:
    headers = {
      'Authorization': 'Bearer ' + config('PAYSTACK_ACCESS_TOKEN')
    }
    endpoint = f'https://api.paystack.co/transferrecipient'
    response = requests.post(endpoint, data=json.dumps(data), headers=headers)
    cache.set(key, response.json())
    return response.json()
  else:
    return value
