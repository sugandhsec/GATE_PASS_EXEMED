# Generated by Django 4.1.6 on 2023-02-03 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_petty_amount_amount_present'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='petty_amount',
            field=models.TextField(default='0'),
        ),
        migrations.AddField(
            model_name='log',
            name='type',
            field=models.TextField(default='Debit'),
        ),
    ]
