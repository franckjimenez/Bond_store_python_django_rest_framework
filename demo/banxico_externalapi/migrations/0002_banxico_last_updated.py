# Generated by Django 3.2.6 on 2021-08-30 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banxico_externalapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banxico',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
