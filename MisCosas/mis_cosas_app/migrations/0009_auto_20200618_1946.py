# Generated by Django 3.0.3 on 2020-06-18 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mis_cosas_app', '0008_remove_item_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='descripcion',
            field=models.CharField(max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='video_id',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
