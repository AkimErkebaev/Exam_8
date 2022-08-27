from django.contrib.auth import get_user_model
from django.db import models

DEFAULT_CATEGORY = 'other'
CATEGORY_CHOICES = (
    (DEFAULT_CATEGORY, 'Разное'),
    ('food', 'Еда'),
    ('tech', 'Бытовая техника'),
    ('tools', 'Инструменты'),
    ('toys', 'Игрушки'),
)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    category = models.CharField(max_length=20, default=DEFAULT_CATEGORY, choices=CATEGORY_CHOICES,
                                verbose_name='Категория')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to="avatars", null=True, blank=True,
                              verbose_name="Картинка")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="orders",
                             verbose_name='Пользователь')
    products = models.ForeignKey('webapp.Product', related_name='orders', verbose_name='Товары',
                                 through='webapp.OrderProduct', through_fields=['order', 'product'])
    otziv = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Отзыв')
    mark = models.PositiveIntegerField(max_length=30, verbose_name='Телефон')
    bool = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return f'{self.user} - {self.products}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
