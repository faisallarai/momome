import json
from decouple import config

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import Group


from rest_framework import status
from rest_framework.test import APITestCase, CoreAPIClient
from payment.helpers import get_digest
from payment.models import Transfer, Transaction, Recipient
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient

from user.models import CustomUser

# Using the standard RequestFactory API to create a form POST request

class PaymentTests(APITestCase):
  token_url = "/auth/token/"

  @classmethod
  def setUpTestData(cls):
    # Set up non-modified objects used by all test methods
    Recipient.objects.create(
      currency = 'GHS',
      recipient_code = 'RCP_fsfa892p5aq6789',
      type = 'mobile_money',
      active = True,
      is_deleted = True,
      account_number = '0244656852',
      name = 'Issaka Faisal',
      account_name = 'Issaka Faisal',
      bank_code = 'MTN',
      bank_name = 'MTN',
      email = 'faisallarai@gmail.com',
      description = ''
    )
    
    user = CustomUser.objects._create_user(
      email = 'test@gmail.com',
      password = 'fsfa892p5aq6789',
    )
    
    administrator = Group.objects.get_or_create(name="administrator")
    print('administrator',administrator)
    print('administrator',administrator[0])
    user.groups.add(administrator[0])
    
  def test_transfer_send(self):
    url = "/payments/transfer/send/"
    data = {
      "account_number": "0241525536",
      "bank_code": "MTN",
      "amount": 210,
      "currency": "GHS",
      "name": "Fadeelatu Issaka",
      "email": "samiraissaka@gmail.com",
      "reason": "Go Live",
      "description": ""
    }
    print(data)
    user_data = {
      'email': 'test@gmail.com',
      'password': 'fsfa892p5aq6789'
    }
    
    auth_resp = self.client.post(self.token_url, data=json.dumps(user_data), content_type='application/json')
    token_data = auth_resp.json()
    token = token_data.get('access')
    print(token)
    headers = {
      "Authorization": "Bearer " + token
    }
    
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    response = client.post(url, data=json.dumps(data), content_type='application/json')
    t_data = response.json()

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(t_data.get('message'), 'Transfer queued successfully.')
    
  def test_transfer_bulk(self):
    url = "/payments/transfer/bulk/"
    data = [
      {
        "account_number": "0244656852",
        "bank_code": "MTN",
        "amount": 100,
        "currency": "GHS",
        "name": "Issaka Faisal",
        "email": "faisallarai@gmail.com",
        "reason": "Go Home",
        "description": ""
      },
      {
          "account_number": "0246559067",
          "bank_code": "MTN",
          "amount": 2000,
          "currency": "GHS",
          "name": "Anissatu Mohammed-Rabiu",
          "email": "anissataymiya@gmail.com",
          "reason": "Go Live",
          "description": ""
      },
      {
          "account_number": "0246181700",
          "bank_code": "MTN",
          "amount": 2000,
          "currency": "GHS",
          "name": "Issaka Samira",
          "email": "samiraissaka@gmail.com",
          "reason": "Go Live",
          "description": ""
      }
    ]
    user_data = {
      'email': 'test@gmail.com',
      'password': 'fsfa892p5aq6789'
    }
    auth_resp = self.client.post(self.token_url, data=json.dumps(user_data), content_type='application/json')
    token_data = auth_resp.json()
    token = token_data.get('access')
    print(token)
    headers = {
      "Authorization": "Bearer " + token
    }
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    response = client.post(url, data=json.dumps(data), content_type='application/json')
    t_data = response.json()
    print('d',t_data)

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(t_data.get('message'), 'Transfers queued successfully.')
    
  def test_webhook_transaction(self):
    url = "/payments/transfer/transaction/"
    data = {
      "event": "transfer.success",
      "data": {
        "amount": 210,
        "createdAt": "2022-11-05T19:20:40.000Z",
        "currency": "GHS",
        "domain": "test",
        "failures": None,
        "id": 198282030,
        "integration": {
          "id": 861088,
          "is_live": False,
          "business_name": "sMart Mart",
          "logo_path": "https://public-files-paystack-prod.s3.eu-west-1.amazonaws.com/integration-logos/paystack.jpg"
        },
        "reason": "Go Live",
        "reference": "aeffb130-127a-4c33-a91c-af0cd4885101",
        "source": "balance",
        "source_details": None,
        "status": "success",
        "titan_code": None,
        "transfer_code": "TRF_wtnv09amqqzwilpb",
        "transferred_at": None,
        "updatedAt": "2022-11-05T19:20:40.000Z",
        "recipient": {
          "active": True,
          "createdAt": "2022-11-04T23:44:44.000Z",
          "currency": "GHS",
          "description": None,
          "domain": "test",
          "email": None,
          "id": 42078771,
          "integration": 861088,
          "metadata": None,
          "name": "Issaka Faisal",
          "recipient_code": "RCP_fsfa892p5aq6789",
          "type": "mobile_money",
          "updatedAt": "2022-11-04T23:44:44.000Z",
          "is_deleted": False,
          "details": {
              "authorization_code": None,
              "account_number": "0244656852",
              "account_name": None,
              "bank_code": "MTN",
              "bank_name": "MTN"
          }
        },
        "session": {
          "provider": None,
          "id": None
        },
        "fee_charged": 0
      }
    }
  
    digest = get_digest(config('PAYSTACK_ACCESS_TOKEN'), data)
    client = APIClient()
    client.credentials(HTTP_x_paystack_signature=digest)
    response = client.post(url, json.dumps(data), content_type='application/json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
