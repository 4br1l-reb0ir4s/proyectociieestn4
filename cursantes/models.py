from django.db import models
from .geof import get_localidades, get_provincias
from .years import get_years, get_years_graduate
from datetime import datetime
# Create your models here.

class NivelEducativo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    class Meta:
        verbose_name = ("Nivel educativo")
        verbose_name_plural= ("Niveles educativos")
    
    def __str__(self):
        return '%s'%(self.nombre)

class Modalidad(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100)

    class Meta:
        verbose_name = ('Modalidad')
        verbose_name_plural = ('Modalidades')

    def __str__(self):
        return '%s'%(self.tipo)
    
class TituloHabilitante(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    nivel_educativo = models.ForeignKey(NivelEducativo, null=True, blank=True, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = ("Título habilitante")
        verbose_name_plural= ("Títulos habilitantes")
    
    def __str__(self):
        return '%s'%(self.nombre)
        # return '{}'.format(self.nombre) Codigo que capaz es util

class Institucion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    modalidad = models.ManyToManyField(Modalidad)
    nivel_educativo = models.ForeignKey(NivelEducativo, null=True, blank=True, on_delete=models.PROTECT)
    cue = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    mail = models.EmailField()
    ciudad = models.CharField(max_length=100, choices=get_localidades(), default="Berazategui")

    class Meta:
        verbose_name = ("Institución")
        verbose_name_plural= ("Instituciones")
    
    def __str__(self):
        return '%s'%( self.nombre)

class Cargo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    nivel_educativo = models.ForeignKey(NivelEducativo, null=True, blank=True, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = ("Cargo")
        verbose_name_plural= ("Cargos")
    
    def __str__(self):
        return '%s'%(self.nombre)

class SituacionRevista(models.Model):
    id = models.AutoField(primary_key=True)
    situacion_revista = models.CharField(max_length=100)

    class Meta:
        verbose_name = ("Situación Revista")
        verbose_name_plural= ("Situaciones Revista")
    
    def __str__(self):
        return '%s'%(self.situacion_revista)


class TipoDispositivo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    resolucion = models.CharField(max_length=100, blank=True, null=True)
    proyecto = models.CharField(max_length=100, blank=True, null=True)
    cantidad_horas = models.CharField(max_length=100, verbose_name="Cantidad horas", default=0)
    dictamen = models.CharField(max_length=100, blank=True, null=True)
    puntaje = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Puntaje", default=0)

    class Meta:
        verbose_name = ('Tipo de Dispositivo')
        verbose_name_plural = ('Tipos de Dispositivo')

    def __str__(self):
        return '%s - %s'%(self.id, self.nombre)

class Formador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    class Meta:
        verbose_name = ("Formador")
        verbose_name_plural= ("Formadores")
    
    def __str__(self):
        return '%s'%(self.nombre)

class Servicios(models.Model): 
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    class Meta:
        verbose_name = ("Servicios")
    
    def __str__(self):
        return '%s'%(self.nombre)
        
class Cohorte(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_servicio = models.ForeignKey(Servicios, null=True, blank=True, on_delete=models.PROTECT)
    ano = models.CharField(max_length=50, choices=get_years(), default=datetime.today().year)
    
    class Meta:
        verbose_name = ("Cohorte")
        verbose_name_plural= ("Cohortes")
    
    def __str__(self):
        return '%s'%( self.nombre_servicio)

class Area(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = ("Área")
        verbose_name_plural= ("Áreas")
    
    def __str__(self):
        return '%s'%( self.nombre)

class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    tipo_dispositivo = models.ForeignKey(TipoDispositivo, null=True, blank=True, on_delete=models.PROTECT)
    cohorte = models.ForeignKey(Cohorte, null=True, blank=True, on_delete=models.PROTECT)
    nombre_formador = models.ForeignKey(Formador, null=True, blank=True, on_delete=models.PROTECT)
    modalidad = models.ForeignKey(Modalidad, null=True, blank=True, on_delete=models.PROTECT)
    area = models.ForeignKey(Area, null=True, blank=True, on_delete=models.PROTECT)
    nivel_educativo = models.ForeignKey(NivelEducativo, null=True, blank=True, on_delete=models.PROTECT)
    carga_horaria = models.CharField(max_length=100, verbose_name="Carga horaria", default=0)
    dias_totales_transcurridos = models.IntegerField(verbose_name="Días totales transcurridos", default=0)

    
    class Meta:
        verbose_name = ("Curso")
        verbose_name_plural= ("Cursos")
    
    def __str__(self):
        return '%s'%(self.tipo_dispositivo)
        
class Cursante(models.Model):
    id = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=100,verbose_name="D.N.I")
    legajo = models.CharField(max_length=20,verbose_name="Legajo",null=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    titulo_habilitante = models.ForeignKey(TituloHabilitante, null=True, blank=True, on_delete=models.PROTECT) 
    ano_egreso = models.CharField(max_length=100, choices=get_years_graduate(), default=datetime.today().year)
    emisor_titulo = models.ForeignKey(Institucion, null=True, blank=True, on_delete=models.PROTECT)
    ciudad = models.CharField(max_length=100, choices=get_localidades(), default="Berazategui")
    direccion = models.CharField(max_length=100, verbose_name="Direccion")
    telefono = models.CharField(max_length=100, verbose_name="Telefono")
    mail_privado = models.EmailField(max_length=254, verbose_name="Mail privado")
    mail_abc = models.EmailField(max_length=254, verbose_name="Mail ABC")
    cargo = models.ForeignKey(Cargo, null=True, blank=True, on_delete=models.PROTECT)
    situacion_revista = models.ForeignKey(SituacionRevista, null=True, blank=True, on_delete=models.PROTECT) 
    titulo_curso_aprobado = models.ForeignKey(Curso, null=True, blank=True, on_delete=models.PROTECT)
    ano_aprobado = models.CharField(max_length=100, choices= get_years(), default=datetime.today().year)
    area_aprobado = models.ForeignKey(Area, null=True, blank=True, on_delete=models.PROTECT)
    cohorte_aprobado = models.ForeignKey(Cohorte, null=True, blank=True, on_delete=models.PROTECT)
    formador_aprobado = models.ForeignKey(Formador, null=True, blank=True, on_delete=models.PROTECT)
    cue = models.ForeignKey(Institucion, verbose_name="CUE", on_delete=models.PROTECT, related_name='get_cue')
    titulos = models.FileField(upload_to='archivo/titulos_validados/', verbose_name="Título")
    
    

    class Meta:
        verbose_name = ("Cursante")
        verbose_name_plural= ("Cursantes")
    
    def __str__(self):
        return '%s - %s'%(self.nombre, self.apellido)


class AsistenciaCursante(models.Model):
    cursante = models.ForeignKey(Cursante, on_delete=models.CASCADE,verbose_name="cursante")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE,verbose_name="curso")
    dias_asistidos = models.PositiveIntegerField(default=0,verbose_name="dias asistidos")

    class Meta:
        unique_together = ('cursante', 'curso')

    def calcular_porcentaje_asistencia(self):
        total_dias = self.curso.dias_totales_transcurridos
        if total_dias > 0:
            porcentaje = (self.dias_asistidos / total_dias) * 100
            return round(porcentaje, 2) 
        else:
            return 0

class AprobadosCursante(models.Model):
    cursante = models.ForeignKey(Cursante, on_delete=models.CASCADE,verbose_name="cursante")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE,verbose_name="curso")
    nota = models.IntegerField(default=False,verbose_name="notas")

    class Meta:
        unique_together=('cursante','curso')