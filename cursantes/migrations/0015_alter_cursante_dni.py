# Generated by Django 4.2.4 on 2023-11-09 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursantes', '0014_alter_cursante_dni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cursante',
            name='dni',
            field=models.IntegerField(verbose_name='D.N.I'),
        ),
    ]
