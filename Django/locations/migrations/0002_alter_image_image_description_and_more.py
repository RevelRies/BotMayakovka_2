# Generated by Django 4.2 on 2023-06-14 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_description',
            field=models.TextField(blank=True, verbose_name='Описание изображения'),
        ),
        migrations.AlterField(
            model_name='location',
            name='next_location_latitude',
            field=models.FloatField(verbose_name='Широта локации'),
        ),
        migrations.AlterField(
            model_name='location',
            name='next_location_longitude',
            field=models.FloatField(verbose_name='Долгота локации'),
        ),
        migrations.AlterField(
            model_name='location',
            name='location_number',
            field=models.IntegerField(verbose_name='Номер локации'),
        ),
    ]
