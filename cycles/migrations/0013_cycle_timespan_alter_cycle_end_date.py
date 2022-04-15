# Generated by Django 4.0.2 on 2022-04-15 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cycles', '0012_alter_income_cycle'),
    ]

    operations = [
        migrations.AddField(
            model_name='cycle',
            name='timespan',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cycle',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
