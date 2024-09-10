from rest_framework import serializers
from transactions.models import Transactions

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'
class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'
