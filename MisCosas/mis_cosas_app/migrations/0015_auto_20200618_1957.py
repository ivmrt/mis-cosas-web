# Generated by Django 3.0.3 on 2020-06-18 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mis_cosas_app', '0014_auto_20200618_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='descripcion',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
