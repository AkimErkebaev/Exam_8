# Generated by Django 4.1 on 2022-08-27 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_rename_products_review_product_alter_review_mark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image', verbose_name='Картинка'),
        ),
    ]
