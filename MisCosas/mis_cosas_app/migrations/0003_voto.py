# Generated by Django 3.0.3 on 2020-06-18 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mis_cosas_app', '0002_remove_alimentador_num_elementos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positivo', models.BooleanField(default=False)),
                ('negativo', models.BooleanField(default=False)),
            ],
        ),
    ]
