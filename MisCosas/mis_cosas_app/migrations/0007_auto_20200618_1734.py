# Generated by Django 3.0.3 on 2020-06-18 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mis_cosas_app', '0006_remove_item_alimentador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='id',
            field=models.CharField(max_length=64, primary_key=True, serialize=False),
        ),
    ]
