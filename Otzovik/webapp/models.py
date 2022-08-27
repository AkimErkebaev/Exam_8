from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


DEFAULT_CATEGORY = 'other'
CATEGORY_CHOICES = (
    (DEFAULT_CATEGORY, 'Разное'),
    ('food', 'Еда'),
    ('drink', 'Напитки'),
    ('zakuski', 'Закуски'),
    ('eat', 'Еда'),
)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    category = models.CharField(max_length=20, default=DEFAULT_CATEGORY, choices=CATEGORY_CHOICES,
                                verbose_name='Категория')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to="image", null=True, blank=True,
                              verbose_name="Картинка")

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("webapp:product_view", kwargs={"pk": self.pk})

    def get_average(self):
        average = self.reviews.mark * len(self.reviews)
        print(average)
        return average["total"]

    class Meta:
        db_table = "products"
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="reviews",
                             verbose_name='Пользователь')
    product = models.ForeignKey('webapp.Product', related_name='reviews',
                                 verbose_name='Продукт', on_delete=models.CASCADE)
    review = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Отзыв')
    mark = models.PositiveIntegerField(verbose_name='оценка')
    bool = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return f'{self.user}'

    # def get_absolute_url(self):
    #     return reverse("webapp:product_view", kwargs={"pk": self.pk})

    class Meta:
        db_table = "reviews"
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
