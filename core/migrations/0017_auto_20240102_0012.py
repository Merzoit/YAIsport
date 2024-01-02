# Generated by Django 3.2.16 on 2024-01-01 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_fixture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixture',
            name='date',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='goals_away',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Голов гостевой команды'),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='goals_home',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Голов домашней команды'),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='league',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.league', verbose_name='Лига'),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='status',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='venue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.venue', verbose_name='Стадион'),
        ),
    ]
