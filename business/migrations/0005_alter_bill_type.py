# Generated by Django 4.2.4 on 2023-08-28 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_location_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='type',
            field=models.CharField(choices=[('TP', 'To Pay'), ('TC', 'To Collect'), ('PA', 'Paid'), ('CO', 'Collected')], max_length=2),
        ),
    ]
