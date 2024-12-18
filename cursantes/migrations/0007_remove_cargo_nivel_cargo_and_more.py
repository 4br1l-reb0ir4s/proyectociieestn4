# Generated by Django 4.0.5 on 2022-11-12 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cursantes', '0006_remove_curso_cursos_febrero_remove_curso_mapda_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cargo',
            name='nivel_cargo',
        ),
        migrations.RemoveField(
            model_name='titulohabilitante',
            name='nivel_titulo',
        ),
        migrations.AddField(
            model_name='cargo',
            name='nivel_educativo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cursantes.niveleducativo'),
        ),
        migrations.AddField(
            model_name='titulohabilitante',
            name='nivel_educativo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cursantes.niveleducativo'),
        ),
    ]
