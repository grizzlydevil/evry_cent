from django.db import models
from django.conf import settings

from cycles.models import Cycle
from banks.models import Account, Vault


class Goal(models.Model):
    """A goal for all containing wallets"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField()

    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)

    percent_of_net = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        default=0.00
    )
    percent_locked = models.BooleanField(default=False)
    money_in = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True,
        default=0.00
    )
    money_in_locked = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs) -> None:
        all_users_goals = self.user.goal_set.order_by('-order')
        if all_users_goals:
            biggest_order = all_users_goals.values()[0]
            self.order = biggest_order + 1
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
    percent_locked = models.BooleanField(default=False)
    money_in = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True,
        default=0.00
    )
    money_in_locked = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs) -> None:
        all_goals_wallets = self.goal.wallet_set.order_by('-order')
        if all_goals_wallets:
            biggest_order = all_goals_wallets.values()[0]
            self.order = biggest_order + 1
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
    percent_locked = models.BooleanField(default=False)
    money_in = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True,
        default=0.00
    )
    money_in_locked = models.BooleanField(default=False)

    in_outside_salary = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00
    )
    in_outside_notes = models.CharField(max_length=160, null=True, blank=True)
    out = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, null=True, blank=True
    )
    out_notes = models.CharField(max_length=160, null=True, blank=True)

    target = models.DecimalField(
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
        all_wallets_pockets = self.wallet.pocket_set.order_by('-order')
        if all_wallets_pockets:
            biggest_order = all_wallets_pockets.values()[0]
            self.order = biggest_order + 1
        else:
            self.order = 1

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title if self.title else self.wallet.title
