from rest_framework import serializers
from .models import Transaction

from payment.serializers import RecipientSerializer

class TransactionSerializer(serializers.ModelSerializer):
  recipient = RecipientSerializer(read_only=True)
  recipient_id = serializers.IntegerField(write_only=True)
  
  class Meta:
    model = Transaction
    fields = '__all__'