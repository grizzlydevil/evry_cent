from django.db import models
from django.conf import settings


class Bank(models.Model):
    """Bank which can contain multiple accounts"""
    class Meta:
        ordering = ['name']

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Account(models.Model):
    """Bank account"""
    class Meta:
        ordering = ['created_at']

    name = models.CharField(max_length=50, null=True, blank=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE,
                             related_name='accounts')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.bank.name} {self.name if self.name else ""} account'


class Vault(models.Model):
    """A bank account might have vaults to split funds in the account"""
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=50)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, blank=True,
        related_name='vaults'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
