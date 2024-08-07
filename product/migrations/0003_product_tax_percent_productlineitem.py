# Generated by Django 5.0.7 on 2024-07-30 05:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_custom_note_alter_product_is_customizable'),
        ('user', '0002_baseuser_valid_otp_alter_baseuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tax_percent',
            field=models.PositiveIntegerField(default=18),
        ),
        migrations.CreateModel(
            name='ProductLineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buying_quantity', models.PositiveIntegerField()),
                ('subtotal', models.PositiveIntegerField(blank=True, null=True)),
                ('total', models.PositiveIntegerField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='related_line_items', to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='related_product_lines', to='user.user')),
            ],
        ),
    ]
