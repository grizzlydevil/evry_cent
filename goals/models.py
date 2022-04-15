from django.db import models
from django.conf import settings

from banks.models import Account, Vault


class Goal(models.Model):
    """A goal that contains wallets"""

    class Meta:
        ordering = ['order']

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=320, null=True, blank=True)

    order = models.PositiveSmallIntegerField(default=1)

    percent_of_net = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        default=0.00
    )
    default_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True,
        default=0.00
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title


class Wallet(models.Model):
    """Wallet is a part of a goal and can contain multiple pockets"""

    class Meta:
        ordering = ['order']

    title = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField()

    goal = models.ForeignKey(
        Goal, on_delete=models.CASCADE, related_name='wallets'
    )

    description = models.TextField(max_length=320, null=True, blank=True)

    percent_of_goal = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        default=0.00
    )
    default_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True,
        default=0.00
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title


class PocketGroup(models.Model):
    """
    A pocket group holds many pockets that are used for the same purpose
    but have different bank accounts or rules to save funds
    """

    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Pocket(models.Model):
    """A pocket is the place where you hold you money"""

    class Meta:
        ordering = ['order']

    title = models.CharField(max_length=50, blank=True, null=True)
    order = models.PositiveSmallIntegerField()

    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='pockets'
    )
    pocket_group = models.ForeignKey(
        PocketGroup, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='pockets'
    )

    description = models.TextField(max_length=320, null=True, blank=True)

    percent_of_wallet = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        default=0.00
    )
    default_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True,
        default=0.00
    )

    save_target = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
    )

    account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True
    )
    vault = models.ForeignKey(
        Vault, on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title if self.title else self.wallet.title


class LendingSlip(models.Model):
    """
    Lend income to another Pocket
    """

    amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00
    )
    sender = models.ForeignKey(
        Pocket, on_delete=models.CASCADE, related_name='sender'
    )
    receiver = models.ForeignKey(
        Pocket, on_delete=models.CASCADE, related_name='receiver'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return (f'{self.sender.title} lended to'
                f'{self.receiver.title}')
