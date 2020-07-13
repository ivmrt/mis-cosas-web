# Generated by Django 3.0.3 on 2020-06-18 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mis_cosas_app', '0013_remove_item_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='descripcion',
            field=models.CharField(default='default', max_length=1024),
        ),
        migrations.AlterField(
            model_name='item',
            name='id',
            field=models.CharField(max_length=64, primary_key=True, serialize=False),
        ),
    ]