# Generated by Django 4.2.4 on 2023-08-02 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_order_location_alter_bill_status_alter_bill_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='total_price',
            field=models.FloatField(default=0.0, editable=False),
        ),
    ]
