# Generated by Django 3.0.3 on 2020-07-15 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mis_cosas_app', '0025_auto_20200715_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='alimentador',
            name='puntuacion',
            field=models.IntegerField(default=0),
        ),
    ]