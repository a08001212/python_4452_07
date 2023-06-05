# Generated by Django 4.2.1 on 2023-06-03 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Daily_transaction_information",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("stock_id", models.CharField(default="0", max_length=10)),
                ("date", models.DateField(auto_now=True)),
                ("TradeVolume", models.IntegerField(default=0)),
                ("HighestPrice", models.FloatField(default=0.0)),
                ("LowestPrice", models.FloatField(default=0.0)),
                ("ClosingPrice", models.FloatField(default=0.0)),
                ("OpeningPrice", models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name="Stock_name",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("stock_id", models.CharField(default="0", max_length=10)),
                ("name", models.CharField(default="undef", max_length=100)),
            ],
        ),
    ]
