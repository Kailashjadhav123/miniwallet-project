from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer, UserSerializer

@api_view(['GET'])
def get_wallet_balance(request):
    wallet = Wallet.objects.get(user=request.user)
    serializer = WalletSerializer(wallet)
    return Response(serializer.data)

class Home(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            balance = Wallet.objects.get(user=request.user)
            serializer = WalletSerializer(balance)
            return Response(serializer.data)
        return Response("Please Login/SignUp")

@api_view(['POST'])
def deposit_to_wallet(request):
    user = request.user
    wallet = Wallet.objects.get(user=user)
    amount = request.data.get('amount')
    Transaction.objects.create(user=user, amount=amount, transaction_type='DEPOSIT')
    return Response({'message': 'Deposit successful'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def withdraw_from_wallet(request):
    wallet = Wallet.objects.get(user=request.user)
    amount = request.data.get('amount')
    if amount <= wallet.balance:
        Transaction.objects.create(user=request.user, amount=amount, transaction_type='WITHDRAW')
        return Response({'message': 'Withdrawal successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_mini_statement(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')[:10]  # Getting last 10 transactions
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def list_all_registered_accounts(request):
    if not request.user.is_superuser:
        return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def list_all_transaction_history(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            transactions = Transaction.objects.all().order_by('-timestamp')
            pagination = PageNumberPagination()
            paginated_queryset = pagination.paginate_queryset(transactions, request)
            serializer = TransactionSerializer(paginated_queryset, many=True)
            return pagination.get_paginated_response(serializer.data)
        else:
            transactions = Transaction.objects.filter(user=request.user)
            pagination = PageNumberPagination()
            paginated_queryset = pagination.paginate_queryset(transactions, request)
            serializer = TransactionSerializer(paginated_queryset, many=True)
            return pagination.get_paginated_response(serializer.data)
    return Response("Please Login/SignUp")