# Generated by Django 3.1.2 on 2021-06-01 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juegos', '0005_auto_20210601_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='juego',
            name='image',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
