# Generated by Django 4.2.1 on 2023-05-21 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_transaction_information',
            name='TradeVolume',
            field=models.IntegerField(default=0),
        ),
    ]
