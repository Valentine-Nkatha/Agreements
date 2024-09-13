from django.test import TestCase

# Create your tests here.
from django.utils import timezone
from .models import Transactions
from decimal import Decimal

class TransactionsModelTest(TestCase):
    def setUp(self):
        self.transaction = Transactions.objects.create(
            unique_code="TXN12345",
            amount=Decimal('150.75'),
            date=timezone.now()
        )

    def test_transaction_creation(self):
        """Test if the transaction is created successfully"""
        self.assertEqual(self.transaction.unique_code, "TXN12345")
        self.assertEqual(self.transaction.amount, Decimal('150.75'))
        self.assertTrue(self.transaction.date)  # Confirming the date is set

    def test_default_values(self):
        """Test default values for fields"""
        transaction = Transactions.objects.create()
        self.assertEqual(transaction.unique_code, "")
        self.assertEqual(transaction.amount, Decimal('0.00'))
        self.assertTrue(isinstance(transaction.date, type(timezone.now())))  # should be timezone aware

    def test_str_method(self):
        """Test the string representation of the transaction"""
        expected_string = f"{self.transaction.amount} {self.transaction.date}"
        self.assertEqual(str(self.transaction), expected_string)