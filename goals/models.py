from django.db import models

from cycles import Cycle


class Goal(models.Model):
    """A goal for all containing wallets"""

    # user field
    title = models.CharField(max_length=50)
    # order = models.SmallAutoField()  # implement increment for every user

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

    def __str__(self) -> str:
        return self.title


class Wallet(models.Model):
    """Wallet is a part of a goal and can contain multiple pockets"""

    title = models.CharField(max_length=50)
    # order = models.SmallAutoField()
    # implement increment for every users Goal

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

    def __str__(self) -> str:
        return self.title


class PocketGroup(models.Model):
    """A pocket group holds many pockets that are used for the same purpose"""

    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.title


class Pocket(models.Model):
    """A pocket is the place where you hold you money"""

    title = models.CharField(max_length=50, blank=True, null=True)
    # order = models.SmallAutoField()  # implement increment for every Wallet

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
    reuse_percent = models.BooleanField(default=False)
    money_in = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True,
        default=0.00
    )
    reuse_money_in = models.BooleanField(default=False)

    in_outside_salary = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00
    )
    in_outside_notes = models.CharField(max_length=160, null=True, blank=True)
    out = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, null=True, blank=True
    )
    out_notes = models.CharField(max_length=160, null=True, blank=True)

    saving = models.BooleanField(default=False)
    target = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True,
    )

    # Bank
    # Account
    # Vault foreignKey on_delete PROTECT?

    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title if self.title else self.wallet.title
