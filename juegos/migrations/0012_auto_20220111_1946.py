# Generated by Django 3.1.2 on 2022-01-11 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juegos', '0011_oferta_property'),
    ]

    operations = [
        migrations.AlterField(
            model_name='juego',
            name='consola',
            field=models.CharField(blank=True, choices=[('nsw', 'SWITCH'), ('ps4', 'PS4'), ('ps5', 'PS5'), ('3ds', '3DS'), ('pc', 'PC'), ('and', 'Android')], max_length=3),
        ),
    ]