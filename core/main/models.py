from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import TextField

User = get_user_model()

class Category(models.Model):
    title = models.CharField(
        max_length=120,
        verbose_name='Название'
    )
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Product(models.Model):
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Продавец"
    )
    name = models.CharField(
        max_length=120,
        verbose_name = 'Название'
    )
    description = models.TextField(
        max_length=300,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Категория'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )

    def __str__(self):
        return str(self.name)

    def get_main_image(self):
        """Возвращает главное изображение продукта, первое изображение, если нет главного, или дефолтное, если вообще нет изображений."""
        main_image = self.images.filter(is_main=True).first()

        if main_image:
            return main_image.file.url
        elif self.images.exists():
            return self.images.first().file.url
        else:
            return "/static/assets/images/defaultimg.png"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Image(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    file = models.ImageField(
        upload_to='product_file',
        verbose_name='Файл'
    )
    is_main = models.BooleanField(default=False, verbose_name="Главное изображение")

    def __str__(self):
        return f"Изображение {self.id} для {self.product.name}"

    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продуктов'

class Rating(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name="Автор отзыва"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name = 'Продукт',
        related_name="ratings"
    )
    count = models.PositiveSmallIntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка'
    )
    text = TextField(
        max_length=200,
        verbose_name='Отзыв'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return str(self.text)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class Reply(models.Model):
    rating = models.ForeignKey(
        Rating,
        on_delete=models.CASCADE,
        related_name="replies"
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="replies",
        verbose_name="Продавец"
    )
    text = models.TextField(
        verbose_name='Ответ'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )
    time_limit = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Ограничение по времени'
    )

    def __str__(self):
        return f"Ответ на отзыв {self.rating.id} от {self.seller.email}"

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

class Order(models.Model):
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Покупатель"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )
    status_choices = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачено'),
        ('shipped', 'Отправлено'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Отменено'),
    ]
    status = models.CharField(
        max_length=20,
        choices=status_choices,
        default='pending',
        verbose_name='Статус заказа'
    )

    @property
    def total_price(self):
        return sum(item.quantity * item.price_at_purchase for item in self.items.all())

    def __str__(self):
        return f"Заказ {self.id} - {self.buyer.email} ({self.get_status_display()})"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    quantity = models.PositiveSmallIntegerField(
        default=1
    )
    price_at_purchase = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Цена на момент покупки"
    )


    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Заказ {self.order.id})"

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'