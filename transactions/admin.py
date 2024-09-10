from django.contrib import admin

# Register your models here.
from .models import Transactions

admin.site.register(Transactions)
# class TransactionsAdmin(admin.ModelAdmin):
#     list_display = ('receipt_id', 'amount', 'code', 'date')