# Generated by Django 3.1.2 on 2021-06-01 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juegos', '0003_auto_20210531_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='juego',
            name='idPrecio',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
