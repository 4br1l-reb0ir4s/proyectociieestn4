# Generated by Django 4.2.4 on 2023-11-22 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursantes', '0021_alter_aprobadoscursante_nota'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aprobadoscursante',
            name='nota',
            field=models.IntegerField(default=False, verbose_name='notas'),
        ),
    ]
