import hashlib
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from agreements.models import Agreements
from decimal import Decimal

class Transactions(models.Model):
    unique_code = models.CharField(max_length=50)
    amount = models.FloatField(default=0.00)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ], default='Pending')
    agreement = models.ForeignKey(
        'agreements.Agreements',
        on_delete=models.CASCADE,
        related_name='transactions',
        null=True,
        blank=True,
        limit_choices_to={'is_active': True}
    )
    previous_hash = models.CharField(max_length=64, blank=True, null=True)
    current_hash = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"{self.amount} {self.date}"

    def clean(self):
        if self.agreement_id == 0:
            raise ValidationError("Agreement ID cannot be zero.")
        
        if self.agreement_id and not Agreements.objects.filter(id=self.agreement_id).exists():
            raise ValidationError(f"No agreement found with ID {self.agreement_id}")

    def save(self, *args, **kwargs):
        self.current_hash = self.generate_hash()

        if self.agreement and self.agreement.transactions.exists():
            last_transaction = self.agreement.transactions.last()
            self.previous_hash = last_transaction.current_hash

        super().save(*args, **kwargs)

        if self.agreement:
            self.agreement.update_on_transaction(self.amount, self.current_hash, self.previous_hash)

    def generate_hash(self):
        transaction_string = f"{self.unique_code}{self.amount}{self.date}{self.status}{self.previous_hash}"
        return hashlib.sha256(transaction_string.encode()).hexdigest()

    def validate_transaction(self):
        if self.current_hash != self.generate_hash():
            self.log_error("Transaction data has been tampered with.")
            raise ValidationError("Transaction data has been tampered with.")

    def log_error(self, message):
        with open("transaction_errors.log", "a") as log_file:
            log_file.write(f"{timezone.now()}: {message}\n")

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(agreement__isnull=True) | models.Q(agreement_id__gt=0),
                name='valid_agreement_reference'
            ),
        ]

    def add_to_blockchain(self):
        if self.agreement:
            transaction_data = {
                'transaction_id': self.id,
                'amount': str(self.amount),
                'timestamp': self.date.timestamp(),
                'current_hash': self.current_hash,
                'previous_hash': self.previous_hash
            }
            self.agreement.add_transaction_to_blockchain(transaction_data)
