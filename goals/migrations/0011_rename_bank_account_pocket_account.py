# Generated by Django 4.0.2 on 2022-04-15 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0010_alter_pocket_pocket_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pocket',
            old_name='bank_account',
            new_name='account',
        ),
    ]
