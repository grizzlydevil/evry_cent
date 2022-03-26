# Generated by Django 4.0.2 on 2022-03-17 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cycles', '0007_remove_income_bank_account_remove_income_cycle_and_more'),
        ('goals', '0005_lendingslip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lendingslip',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='lendingslip',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='pocket',
            name='bank_account',
        ),
        migrations.RemoveField(
            model_name='pocket',
            name='pocket_group',
        ),
        migrations.RemoveField(
            model_name='pocket',
            name='vault',
        ),
        migrations.RemoveField(
            model_name='pocket',
            name='wallet',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='goal',
        ),
        migrations.DeleteModel(
            name='Goal',
        ),
        migrations.DeleteModel(
            name='LendingSlip',
        ),
        migrations.DeleteModel(
            name='Pocket',
        ),
        migrations.DeleteModel(
            name='PocketGroup',
        ),
        migrations.DeleteModel(
            name='Wallet',
        ),
    ]