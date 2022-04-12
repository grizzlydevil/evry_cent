from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Bank, Account, Vault
from .serializers import BankSerializer, AccountSerializer, VaultSerializer


class BankViewSet(viewsets.ModelViewSet):
    """CRUD Banks"""

    permission_classes = (IsAuthenticated,)
    serializer_class = BankSerializer

    def get_queryset(self):
        """get current users banks"""
        return Bank.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """add current user to serializer"""
        serializer.save(user=self.request.user)


class AccountViewSet(viewsets.ModelViewSet):
    """CRUD Accounts"""

    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer

    def get_queryset(self):
        """get current users banks"""
        return Account.objects.filter(bank__user=self.request.user)


class VaultViewSet(viewsets.ModelViewSet):
    """CRUD Vaults"""

    permission_classes = (IsAuthenticated,)
    serializer_class = VaultSerializer

    def get_queryset(self):
        """get current users banks"""
        return Vault.objects.filter(account__bank__user=self.request.user)
