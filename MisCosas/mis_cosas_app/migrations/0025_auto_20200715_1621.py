# Generated by Django 3.0.3 on 2020-07-15 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mis_cosas_app', '0024_item_puntuacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='puntuacion',
            field=models.IntegerField(default=0),
        ),
    ]
