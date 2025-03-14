# Generated by Django 5.1.6 on 2025-03-10 15:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_image_is_main'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='sells', to=settings.AUTH_USER_MODEL, verbose_name='Продавец'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('in_cart', 'В корзине'), ('pending', 'Ожидает оплаты'), ('paid', 'Оплачено'), ('shipped', 'Отправлено'), ('delivered', 'Доставлено'), ('cancelled', 'Отменено')], default='in_cart', max_length=20, verbose_name='Статус заказа'),
        ),
    ]
