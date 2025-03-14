# Generated by Django 5.1.6 on 2025-03-11 09:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_payment_order_payment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Оплата', 'verbose_name_plural': 'Оплаты'},
        ),
        migrations.AddField(
            model_name='payment',
            name='receipt',
            field=models.FileField(blank=True, null=True, upload_to='receipts/'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='main.payment'),
        ),
    ]
