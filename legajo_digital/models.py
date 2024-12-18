from django.db import models
from cursantes.models import datetime, Institucion, Cargo, SituacionRevista
from cursantes.years import get_years, get_years_graduate
from cursantes.geof import get_localidades

class Aspirante(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    dni = models.CharField(max_length=100,verbose_name="D.N.I")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    ano_egreso = models.CharField(max_length=100, choices=get_years_graduate(), default=datetime.today().year)
    emisor_titulo = models.ForeignKey(Institucion, null=True, blank=True, on_delete=models.PROTECT)
    ciudad = models.CharField(max_length=100, choices=get_localidades(), default="Berazategui")
    direccion = models.CharField(max_length=100, verbose_name="Direccion")
    telefono = models.CharField(max_length=100, verbose_name="Telefono")
    mail_privado = models.EmailField(max_length=254, verbose_name="Mail privado")
    mail_abc = models.EmailField(max_length=254, verbose_name="Mail ABC")
    cargo = models.ForeignKey(Cargo, null=True, blank=True, on_delete=models.PROTECT)
    situacion_revista = models.ForeignKey(SituacionRevista, null=True, blank=True, on_delete=models.PROTECT)
    cue = models.ForeignKey(Institucion, verbose_name="CUE", on_delete=models.PROTECT, related_name='get_cue_aspirante')
    titulos = models.FileField(upload_to='archivos/titulos/', verbose_name="Títulos")