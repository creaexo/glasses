# Generated by Django 4.1.4 on 2023-06-15 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('glasses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Glasses_form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Форма оправы',
                'verbose_name_plural': 'Форма оправ',
            },
        ),
        migrations.CreateModel(
            name='Glasses_frame_material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Материал оправы',
                'verbose_name_plural': 'Материалы оправ',
            },
        ),
        migrations.CreateModel(
            name='Glasses_frame_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Тип оправы',
                'verbose_name_plural': 'Типы оправ',
            },
        ),
        migrations.CreateModel(
            name='Glasses_gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Пол',
                'verbose_name_plural': 'Пол',
            },
        ),
        migrations.CreateModel(
            name='Glasses_linces_ax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Ось (Ax)')),
            ],
            options={
                'verbose_name': 'Ось (Ax)',
                'verbose_name_plural': 'Ось (Ax)',
            },
        ),
        migrations.CreateModel(
            name='Glasses_linces_cyl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='Цилиндр (Cyl)')),
            ],
            options={
                'verbose_name': 'Цилиндр (Cyl)',
                'verbose_name_plural': 'Цилиндр (Cyl)',
            },
        ),
        migrations.CreateModel(
            name='Glasses_linces_pd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='РМЦ (PD)')),
            ],
            options={
                'verbose_name': 'РМЦ (PD)',
                'verbose_name_plural': 'РМЦ (PD)',
            },
        ),
        migrations.CreateModel(
            name='Glasses_linces_sph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='Сфера (Sph)')),
            ],
            options={
                'verbose_name': 'Сфера (Sph)',
                'verbose_name_plural': 'Сфера (Sph)',
            },
        ),
        migrations.CreateModel(
            name='Glasses_manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Производитель',
                'verbose_name_plural': 'Производители',
            },
        ),
        migrations.CreateModel(
            name='Glasses_size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=5)),
            ],
            options={
                'verbose_name': 'Размер очков',
                'verbose_name_plural': 'Размеры очков',
            },
        ),
        migrations.CreateModel(
            name='Glasses',
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
                ('Lenses_height', models.IntegerField(verbose_name='Высота линзы')),
                ('Lenses_width', models.IntegerField(verbose_name='Ширина линзы')),
                ('Lenses_length', models.IntegerField(verbose_name='Длина линзы')),
                ('Lenses_bridge', models.IntegerField(verbose_name='Высота линзы')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='glasses.category', verbose_name='Категория')),
                ('frame_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_glasses.glasses_frame_material', verbose_name='Материал оправы')),
                ('frame_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_glasses.glasses_frame_type', verbose_name='Тип оправы')),
                ('glasses_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_glasses.glasses_form', verbose_name='Форма очков')),
                ('glasses_gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_glasses.glasses_gender', verbose_name='Пол')),
                ('glasses_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_glasses.glasses_size', verbose_name='Размер очков')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_glasses.glasses_manufacturer', verbose_name='Производитель')),
            ],
            options={
                'verbose_name': '    Оправы',
                'verbose_name_plural': ' Оправы',
            },
        ),
    ]