# Generated by Django 3.2.6 on 2021-08-27 21:22

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bond',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=40)),
                ('total_sell', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(10000), django.core.validators.MinValueValidator(1)])),
                ('price_total', models.DecimalField(decimal_places=4, default=0.0, max_digits=13, validators=[django.core.validators.MaxValueValidator(Decimal('100000000.0000')), django.core.validators.MinValueValidator(Decimal('0.0000'))])),
            ],
            options={
                'verbose_name': 'Bond',
                'verbose_name_plural': 'Bonds',
                'ordering': ['id'],
            },
        ),
    ]
