from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('balance/', get_wallet_balance, name='balance'),
    path('deposit/', deposit_to_wallet, name='deposit'),
    path('withdraw/', withdraw_from_wallet, name='withdraw'),
    path('statement/', get_mini_statement, name='statement'),
    path('accounts/', list_all_registered_accounts, name='accounts'),
    path('transactions/', list_all_transaction_history, name='transactions')
]