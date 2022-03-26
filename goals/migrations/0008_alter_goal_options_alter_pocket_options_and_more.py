# Generated by Django 4.0.2 on 2022-03-26 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0007_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goal',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='pocket',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='wallet',
            options={'ordering': ['order']},
        ),
        migrations.AlterField(
            model_name='pocket',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pockets', to='goals.wallet'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='goal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallets', to='goals.goal'),
        ),
    ]