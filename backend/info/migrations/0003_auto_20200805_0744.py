# Generated by Django 2.2.15 on 2020-08-05 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_auto_20200804_2138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tokenizedadress',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='tokenizedadress',
            name='answer_body',
        ),
    ]