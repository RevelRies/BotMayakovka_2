# Generated by Django 4.2 on 2023-06-21 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0008_location_next_button_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_tg_id', models.IntegerField(verbose_name='id пользователя в телеграме')),
                ('full_name', models.TextField(default='', verbose_name='Имя пользователя при наличии')),
                ('username', models.TextField(default='', verbose_name='Юзернейм пользователя при наличии')),
                ('reg_time', models.DateTimeField(verbose_name='Дата регистрации пользователя')),
                ('last_time', models.DateTimeField(verbose_name='Дата последнего действия пользователя')),
                ('counter_locations', models.IntegerField(default=0, verbose_name='Количество пройденных локаций')),
            ],
        ),
        migrations.AlterField(
            model_name='location',
            name='next_location_latitude',
            field=models.FloatField(verbose_name='Широта следующей локации'),
        ),
        migrations.AlterField(
            model_name='location',
            name='next_location_longitude',
            field=models.FloatField(verbose_name='Долгота следующей локации'),
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_name', models.TextField(verbose_name='Название выполненной команды')),
                ('click_time', models.DateTimeField(verbose_name='время и дата выполненной команды')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.user', verbose_name='Пользователь который совершил действие')),
            ],
        ),
    ]
