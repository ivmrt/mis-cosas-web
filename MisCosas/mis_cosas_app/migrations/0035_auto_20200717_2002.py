# Generated by Django 3.0.3 on 2020-07-17 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mis_cosas_app', '0034_auto_20200717_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='foto',
            field=models.ImageField(default='media/PERFIL-HUEVO.jpg', upload_to='media/'),
        ),
        migrations.DeleteModel(
            name='FotodePerfil',
        ),
    ]
