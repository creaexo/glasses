# Generated by Django 4.1.4 on 2023-06-15 03:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('glasses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lenses_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Категории линз',
                'verbose_name_plural': 'Категории линз',
            },
        ),
        migrations.CreateModel(
            name='Lenses_manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Производитель линз',
                'verbose_name_plural': 'Производители линз',
            },
        ),
        migrations.CreateModel(
            name='Lenses_material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Материал линз',
                'verbose_name_plural': 'Материалы линз',
            },
        ),
        migrations.CreateModel(
            name='Lenses_rad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='Радиус (Вс)')),
            ],
            options={
                'verbose_name': 'Радиус линз',
                'verbose_name_plural': 'Радиусы линз',
            },
        ),
        migrations.CreateModel(
            name='Lenses_Sph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='Сфера (Sph)')),
            ],
            options={
                'verbose_name': 'Сфера линз',
                'verbose_name_plural': 'Сферы линз',
            },
        ),
        migrations.CreateModel(
            name='Lenses_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Тип линз',
                'verbose_name_plural': 'Типы линз',
            },
        ),
        migrations.CreateModel(
            name='Lenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('slug', models.SlugField(unique=True)),
                ('image1', models.ImageField(blank=True, upload_to='', verbose_name='Изображение 1')),
                ('image2', models.ImageField(blank=True, upload_to='', verbose_name='Изображение 2')),
                ('image3', models.ImageField(blank=True, upload_to='', verbose_name='Изображение 3')),
                ('image4', models.ImageField(blank=True, upload_to='', verbose_name='Изображение 4')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('meaning', models.BooleanField(default=0, verbose_name='UVA/UVB защита')),
                ('moisture', models.IntegerField(validators=[django.core.validators.MaxValueValidator(100)], verbose_name='Влагосодержание')),
                ('oxygen', models.IntegerField(verbose_name='Пропускание кислорода (Dk/t)')),
                ('diameter', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Диаметр')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='glasses.category', verbose_name='Категория')),
                ('category_of_lenses', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='product_lenses.lenses_category', verbose_name='Категория линз')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_lenses.lenses_manufacturer', verbose_name='Производитель')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_lenses.lenses_material', verbose_name='Материал')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_lenses.lenses_type', verbose_name='Тип')),
            ],
            options={
                'verbose_name': '    Линзы',
                'verbose_name_plural': ' Линзы',
            },
        ),
    ]