# Generated by Django 5.1.1 on 2024-11-03 00:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_cart_id_alter_cartitem_cart_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
