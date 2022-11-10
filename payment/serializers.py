from rest_framework import serializers

from .models import Transfer, Recipient

    
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
