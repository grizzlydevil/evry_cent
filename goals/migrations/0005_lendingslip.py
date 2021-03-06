# Generated by Django 4.0.2 on 2022-03-15 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0004_pocket_bank_account_pocket_vault'),
    ]

    operations = [
        migrations.CreateModel(
            name='LendingSlip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='goals.pocket')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='goals.pocket')),
            ],
        ),
    ]
