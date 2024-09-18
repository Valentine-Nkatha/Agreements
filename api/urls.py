from django.urls import path
from .views import TransactionsListView,AgreementsView,AgreementDetailView,CheckBlockchainView

urlpatterns =[
   path("transactions/",TransactionsListView.as_view(), name="transactions_list_view"),
   path('agreements/', AgreementsView.as_view(), name='agreements_list'),
    path('agreements/<int:id>/', AgreementDetailView.as_view(), name='agreement_detail'),
    path('check-blockchain/', CheckBlockchainView.as_view(), name='check_blockchain'),
]