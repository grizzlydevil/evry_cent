# Generated by Django 4.0.2 on 2022-03-14 20:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0002_remove_pocket_bank_account_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('order', models.PositiveSmallIntegerField(default=1)),
                ('percent_of_net', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5, null=True)),
                ('default_amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PocketGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('order', models.PositiveSmallIntegerField()),
                ('description', models.TextField(max_length=320)),
                ('percent_of_goal', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5, null=True)),
                ('default_amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goals.goal')),
            ],
        ),
        migrations.CreateModel(
            name='Pocket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('order', models.PositiveSmallIntegerField()),
                ('description', models.TextField(max_length=320)),
                ('percent_of_wallet', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5, null=True)),
                ('default_amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('save_target', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('pocket_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='goals.pocketgroup')),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goals.wallet')),
            ],
        ),
    ]
