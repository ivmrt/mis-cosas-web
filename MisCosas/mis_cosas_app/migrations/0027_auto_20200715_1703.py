# Generated by Django 3.0.3 on 2020-07-15 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mis_cosas_app', '0026_alimentador_puntuacion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alimentador',
            old_name='puntuacion',
            new_name='votos',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='puntuacion',
            new_name='votos',
        ),
    ]
