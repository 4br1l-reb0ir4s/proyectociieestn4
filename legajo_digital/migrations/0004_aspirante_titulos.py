# Generated by Django 4.2.5 on 2023-11-21 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legajo_digital', '0003_alter_aspirante_dni'),
    ]

    operations = [
        migrations.AddField(
            model_name='aspirante',
            name='titulos',
            field=models.FileField(default=1, upload_to='archivos/titulos/', verbose_name='Títulos'),
            preserve_default=False,
        ),
    ]
