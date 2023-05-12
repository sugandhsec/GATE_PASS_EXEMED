# Generated by Django 4.0.4 on 2023-05-12 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0024_user_rgp_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='nrgp_entry',
            name='nrgp_main_serial',
            field=models.CharField(default=0, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user_rgp',
            name='department',
            field=models.CharField(choices=[('admin', 'admin'), ('HR', 'HR'), ('QA', 'QA'), ('QC', 'QC'), ('PH', 'PH'), ('WH', 'WH'), ('ENGG', 'ENGG'), ('API', 'API'), ('ADL', 'ADL'), ('EOHS', 'EOHS'), ('IT', 'IT')], max_length=100, null=True),
        ),
    ]
