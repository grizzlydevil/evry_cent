# Generated by Django 4.0.2 on 2022-04-15 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cycles', '0009_rename_cash_income_is_cash'),
    ]

    operations = [
        migrations.RenameField(
            model_name='income',
            old_name='bank_account',
            new_name='account',
        ),
    ]
