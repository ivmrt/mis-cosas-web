# Generated by Django 3.0.3 on 2020-07-15 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mis_cosas_app', '0027_auto_20200715_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='foto',
            field=models.URLField(null=True),
        ),
    ]
