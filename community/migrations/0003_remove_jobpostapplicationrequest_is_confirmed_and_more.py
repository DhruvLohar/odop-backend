# Generated by Django 5.0.7 on 2024-07-30 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_jobpostapplicationrequest_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobpostapplicationrequest',
            name='is_confirmed',
        ),
        migrations.RemoveField(
            model_name='rentalmachinebookingrequest',
            name='is_confirmed',
        ),
        migrations.AddField(
            model_name='jobpostapplicationrequest',
            name='status',
            field=models.CharField(choices=[('PEN', 'Pending'), ('APR', 'Approved'), ('CAN', 'Cancelled')], default='PEN', max_length=20),
        ),
        migrations.AddField(
            model_name='rentalmachinebookingrequest',
            name='status',
            field=models.CharField(choices=[('PEN', 'Pending'), ('APR', 'Approved'), ('CAN', 'Cancelled')], default='PEN', max_length=20),
        ),
    ]
