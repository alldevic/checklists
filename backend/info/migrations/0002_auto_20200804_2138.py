# Generated by Django 2.2.15 on 2020-08-04 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenizedadress',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='tokenizedadress',
            name='house',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Дом'),
        ),
        migrations.AlterField(
            model_name='tokenizedadress',
            name='postal_code',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='Индекс'),
        ),
        migrations.AlterField(
            model_name='tokenizedadress',
            name='region',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Регион'),
        ),
        migrations.AlterField(
            model_name='tokenizedadress',
            name='street',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Улица'),
        ),
    ]
