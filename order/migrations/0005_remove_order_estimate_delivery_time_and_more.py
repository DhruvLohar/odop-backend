# Generated by Django 5.0.7 on 2024-07-30 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_orderlineitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='estimate_delivery_time',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AddField(
            model_name='orderlineitem',
            name='estimate_delivery_time',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderlineitem',
            name='status',
            field=models.CharField(choices=[('PEN', 'Pending'), ('CON', 'Confirmed'), ('SHP', 'Shipped'), ('DLV', 'Delivered'), ('RFI', 'Refund Initiated'), ('RFP', 'Refund In Process'), ('RFS', 'Refund Successs'), ('RFC', 'Refund Cancelled'), ('CAN', 'Cancelled')], default='PEN', max_length=50),
        ),
    ]
