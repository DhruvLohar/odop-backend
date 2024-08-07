# Generated by Django 5.0.7 on 2024-07-30 06:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('artisan', '0002_artisan_verified_by_authority'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('address', models.TextField()),
                ('date', models.DateTimeField()),
                ('tags', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('address', models.TextField()),
                ('date', models.DateTimeField()),
                ('workshop_level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advance', 'Advance')], max_length=50)),
                ('tags', models.JSONField(default=list)),
                ('organized_by', models.CharField(max_length=200)),
                ('conducted_by_artisan', models.BooleanField(default=False)),
                ('price', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('artisan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='conducted_workshops', to='artisan.artisan')),
            ],
        ),
    ]
