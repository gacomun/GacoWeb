# Generated by Django 3.1.2 on 2021-05-31 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juegos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='juego',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]
