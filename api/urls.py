from django.urls import path
from .views import TransactionsListView, NotificationsListView, TransactionsSearchView, TransactionsDetailView

urlpatterns =[
   path("transactions/",TransactionsListView.as_view(), name="transactions_list_view"),
   path("notifications/",NotificationsListView.as_view(), name="notifications_list_view"),
   path("transactions/search/",TransactionsSearchView.as_view(),name="transactions_search_view"),
   path("transactions/<int:id>/", TransactionsDetailView.as_view(), name="transactions_detail_view"),
]