# Generated by Django 4.1 on 2022-08-27 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('other', 'Разное'), ('food', 'Еда'), ('drink', 'Напитки'), ('zakuski', 'Закуски'), ('eat', 'Еда')], default='other', max_length=20, verbose_name='Категория'),
        ),
    ]
