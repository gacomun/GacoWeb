# Generated by Django 3.1.2 on 2021-05-31 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juegos', '0002_juego_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='juego',
            name='precio',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='juego',
            name='venta',
            field=models.BooleanField(default=False),
        ),
    ]
