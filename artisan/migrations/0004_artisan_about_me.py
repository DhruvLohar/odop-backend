# Generated by Django 5.0.7 on 2024-08-22 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artisan', '0003_remove_artisan_date_of_birth_artisan_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='artisan',
            name='about_me',
            field=models.TextField(default='hello'),
            preserve_default=False,
        ),
    ]