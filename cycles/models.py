from django.db import models


class Cycle(models.Model):
    """
    A cycle is a sum of all incomes over a timespan between two dates.
    Usually a cycle should last 1 month. But the timespan is not mandatory.
    All the funds from one cycle are being distributed over all of the goals.
    """

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self) -> str:
        return (
            f'{self.start_date.strftime("%Y-%m-%d")} - '
            f'{self.end_date.strftime("%Y-%m-%d")}'
        )


class Income(models.Model):
    """
    An income which will be split for the goals
    """

    title = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)

    # bank account

    def __str__(self):
        return self.title