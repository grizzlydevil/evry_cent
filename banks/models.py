from django.db import models


class Bank(models.Model):
    """Bank which can contain multiple accounts"""

    # USER
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Account(models.Model):
    """Bank account"""

    name = models.CharField(max_length=50, null=True, blank=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.bank.name} ' + self.name if self.name else 'account'


class Vault(models.Model):
    """A bank account might have vaults to split funds in the account"""

    name = models.CharField(max_length=50)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.name
