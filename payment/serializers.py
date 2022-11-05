from rest_framework import serializers

from .models import Transfer, Transaction, Recipient

    
class RecipientSerializer(serializers.ModelSerializer):

  class Meta:
    model = Recipient
    fields = '__all__'
    
class TransferSerializer(serializers.ModelSerializer):
  recipient = RecipientSerializer(read_only=True)
  recipient_id = serializers.IntegerField(write_only=True)
  
  class Meta:
    model = Transfer
    fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
  recipient = RecipientSerializer(read_only=True)
  recipient_id = serializers.IntegerField(write_only=True)
  transfer = TransferSerializer(read_only=True)
  transfer_id = serializers.IntegerField(write_only=True)

  class Meta:
    model = Transaction
    fields = '__all__'
    