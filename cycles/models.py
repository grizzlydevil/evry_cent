from django.db import models
from django.conf import settings

from banks.models import Account
from goals.models import Pocket


class Cycle(models.Model):
    """
    A cycle is a sum of all incomes over a timespan between two dates.
    Usually a cycle should last 1 month. But the timespan is not mandatory.
    All the funds from one cycle are being distributed over all of the goals.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    timespan = models.DurationField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return (
            f'{self.start_date.strftime("%Y-%m-%d")}' +
            f' - {self.end_date.strftime("%Y-%m-%d")}' if self.end_date else ''
        )


class Income(models.Model):
    """
    An income which will be split for the goals.
    One or more incomes can exist in a single cycle.
    """

    title = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE,
                              related_name='incomes')

    account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class IncomeDistributor(models.Model):
    """
    Distributes money from a single Cycle to all the Pockets
    There is a single IncomeDistributor for every Pocket
    """

    cycle = models.ForeignKey(
        Cycle, on_delete=models.CASCADE, related_name='distributors'
    )
    pocket = models.ForeignKey(Pocket, on_delete=models.CASCADE,
                               related_name='distributors')

    money_in = models.DecimalField(
        max_digits=12, decimal_places=2,
        default=0.00
    )

    in_outside_salary = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00
    )
    in_outside_notes = models.CharField(max_length=160, null=True, blank=True)

    out = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00
    )
    out_notes = models.CharField(max_length=160, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.pocket.title} distributor'


class IncomeLendingSlip(models.Model):
    """
    Lend income to another Pocket
    """

    amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00
    )
    sender = models.ForeignKey(
        IncomeDistributor, on_delete=models.CASCADE, related_name='sender'
    )
    receiver = models.ForeignKey(
        IncomeDistributor, on_delete=models.CASCADE, related_name='receiver'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return (f'{self.sender.pocket.title} lended to'
                f'{self.receiver.pocket.title}')
