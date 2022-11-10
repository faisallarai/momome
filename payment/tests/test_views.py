import json
from decouple import config

from django.urls import reverse
from django.contrib.auth.models import Group


from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from payment.models import Recipient
from rest_framework.test import force_authenticate

from user.models import CustomUser

# Using the standard RequestFactory API to create a form POST request

class PaymentTests(APITestCase):
  token_url = "/auth/token/"

  @classmethod
  def setUpTestData(cls):
    # Set up non-modified objects used by all test methods
    
    user = CustomUser.objects._create_user(
      email = 'test@gmail.com',
      password = 'fsfa892p5aq6789',
    )
    
    administrator = Group.objects.get_or_create(name="administrator")
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
    user_data = {
      'email': 'test@gmail.com',
      'password': 'fsfa892p5aq6789'
    }
    
    auth_resp = self.client.post(self.token_url, data=json.dumps(user_data), content_type='application/json')
    token_data = auth_resp.json()
    token = token_data.get('access')
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
    
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    response = client.post(url, data=json.dumps(data), content_type='application/json')
    t_data = response.json()

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(t_data.get('message'), 'Transfers queued successfully.')
