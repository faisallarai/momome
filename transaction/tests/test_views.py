import json
from decouple import config

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from transaction.helpers import get_digest
from payment.models import Recipient

class TransactionViewTests(APITestCase):
  @classmethod
  def setUpTestData(cls):
    Recipient.objects.get_or_create(
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
  def test_webhook_transaction(self):
    url = "/transactions/"
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
          "email": "faisallarai@gmail.com",
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