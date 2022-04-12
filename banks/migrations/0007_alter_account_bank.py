# Generated by Django 4.0.2 on 2022-04-12 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banks', '0006_alter_account_options_alter_bank_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='bank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='banks.bank'),
        ),
    ]