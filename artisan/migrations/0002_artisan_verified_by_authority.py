# Generated by Django 5.0.7 on 2024-07-29 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artisan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artisan',
            name='verified_by_authority',
            field=models.BooleanField(default=False),
        ),
    ]