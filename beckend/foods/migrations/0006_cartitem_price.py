# Generated by Django 5.1 on 2025-01-07 09:12

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0005_cart_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10, verbose_name='Цена'),
        ),
    ]
