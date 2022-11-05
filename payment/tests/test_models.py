from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from payment.models import Recipient


class RecipientModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    # Set up non-modified objects used by all test methods
    Recipient.objects.create(
      currency = 'GHS',
      recipient_code = 'RCP_fsfa892p5aq9876',
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

  def test_currency_label(self):
    recipient = Recipient.objects.get(id=1)
    field_label = recipient._meta.get_field('currency').verbose_name
    self.assertEqual(field_label, 'currency')
  
  def test_currency_max_length(self):
    recipient = Recipient.objects.get(id=1)
    max_length = recipient._meta.get_field('currency').max_length
    self.assertEqual(max_length, 5)

  def test_recipient_code_label(self):
    recipient = Recipient.objects.get(id=1)
    field_label = recipient._meta.get_field('recipient_code').verbose_name
    self.assertEqual(field_label, 'recipient code')

  def test_recipient_code_max_length(self):
    recipient = Recipient.objects.get(id=1)
    max_length = recipient._meta.get_field('recipient_code').max_length
    self.assertEqual(max_length, 50)
