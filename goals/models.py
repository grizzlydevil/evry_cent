from django.db import models
from django.conf import settings

from banks.models import Account, Vault


class Goal(models.Model):
    """A goal for all containing wallets"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50)
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

    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs) -> None:
        last_order_goal = self.user.goal_set.order_by('-order').first()
        if last_order_goal:
            self.order = last_order_goal.order + 1
        else:
            self.order = 1

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Wallet(models.Model):
    """Wallet is a part of a goal and can contain multiple pockets"""

    title = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField()

    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)

    description = models.TextField(max_length=320)

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

    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs) -> None:
        last_order_wallet = self.goal.wallet_set.order_by('-order').first()
        if last_order_wallet:
            self.order = last_order_wallet.order + 1
        else:
            self.order = 1

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class PocketGroup(models.Model):
    """
    A pocket group holds many pockets that are used for the same purpose
    but have different bank accounts or rules to save funds
    """

    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.title


class Pocket(models.Model):
    """A pocket is the place where you hold you money"""

    title = models.CharField(max_length=50, blank=True, null=True)
    order = models.PositiveSmallIntegerField()

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    pocket_group = models.ForeignKey(
        PocketGroup, on_delete=models.SET_NULL, null=True, blank=True
    )

    description = models.TextField(max_length=320)

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

    bank_account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True
    )
    vault = models.ForeignKey(
        Vault, on_delete=models.SET_NULL, null=True, blank=True
    )

    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs) -> None:
        last_order_pocket = self.wallet.pocket_set.order_by('-order').first()
        if last_order_pocket:
            self.order = last_order_pocket.order + 1
        else:
            self.order = 1

        super().save(*args, **kwargs)

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

    date_created = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=True)
