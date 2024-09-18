from rest_framework import serializers
from transactions.models import Transactions
from agreements.models import Agreements

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'
class AgreementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreements
        fields = '__all__'
class BlockchainValidationSerializer(serializers.Serializer):
    validation_result = serializers.CharField()