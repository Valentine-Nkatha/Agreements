# agreements/models.py

from django.db import models
from datetime import datetime
from transactions.blockchain import Blockchain
import hashlib
import json

class Agreements(models.Model):
    date_created = models.DateField(auto_now_add=True)
    contract_duration = models.PositiveSmallIntegerField()
    agreed_amount = models.PositiveIntegerField()
    installment_schedule = models.TextField()
    penalties_interest_rate = models.PositiveIntegerField()
    down_payment = models.PositiveIntegerField()
    buyer_agreed = models.BooleanField(default=False)
    seller_agreed = models.BooleanField(default=False)
    terms_and_conditions = models.TextField(default="No terms and conditions provided.")
    transaction_count = models.PositiveIntegerField(default=0)
    remaining_amount = models.FloatField(default=0.00)
    total_amount_made = models.FloatField(default=0.00)
    agreement_hash = models.CharField(max_length=64, blank=True, null=True)
    transactions_history = models.JSONField(default=list, blank=True)

    blockchain = Blockchain()

    def generate_hash(self, transaction_data):
        transaction_string = json.dumps(transaction_data, sort_keys=True).encode()
        return hashlib.sha256(transaction_string).hexdigest()

    def update_on_transaction(self, transaction_amount):
        self.transaction_count += 1
        self.total_amount_made += transaction_amount
        self.remaining_amount = self.agreed_amount - self.total_amount_made

        transaction_data = {
            'amount': transaction_amount,
            'timestamp': datetime.now().isoformat(),
            'transaction_count': self.transaction_count,
        }

        previous_hash = None
        if self.transactions_history:
            previous_transaction = self.transactions_history[-1]
            previous_hash = previous_transaction['current_hash']

        current_hash = self.generate_hash(transaction_data)

        transaction_data['current_hash'] = current_hash
        transaction_data['previous_hash'] = previous_hash
        self.save()

        self.transactions_history.append(transaction_data)
        self.save(update_fields=['transactions_history'])

        self.add_transaction_to_blockchain(transaction_data)

    def add_transaction_to_blockchain(self, transaction):
        self.blockchain.add_transaction(transaction)

    def __str__(self):
        return f"{self.agreed_amount} {self.date_created}"
