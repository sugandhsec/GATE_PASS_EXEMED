# Generated by Django 4.1.1 on 2023-03-02 04:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_nrgp_entry_unit'),
    ]

    operations = [
        migrations.DeleteModel(
            name='log',
        ),
        migrations.DeleteModel(
            name='petty_amount',
        ),
    ]
