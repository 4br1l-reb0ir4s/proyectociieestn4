import django_filters
from django import forms
from cursantes.models import Cursante, Curso, Formador, Institucion, Modalidad, SituacionRevista, TipoDispositivo, TituloHabilitante, Cohorte, Cargo, Area, Servicios, NivelEducativo,AsistenciaCursante

class AspiranteFilter(django_filters.FilterSet):
    
    nombre = django_filters.CharFilter(label='Nombre', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    apellido = django_filters.CharFilter(label='Apellido', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    ano_egreso = django_filters.CharFilter(label='Año de egreso', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    emisor_titulo = django_filters.ModelChoiceFilter(label='Emisor del titulo', queryset=Institucion.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    ciudad = django_filters.CharFilter(label='Ciudad', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    direccion = django_filters.CharFilter(label='Direccion', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    telefono = django_filters.CharFilter(label='Telefono', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    mail_privado = django_filters.CharFilter(label='Mail privado', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    mail_abc = django_filters.CharFilter(label='Mail ABC', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    cargo  = django_filters.ModelChoiceFilter(label='Cargo', queryset=Cargo.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    situacion_revista = django_filters.ModelChoiceFilter(label='Situación de Revista', queryset=SituacionRevista.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    cue = django_filters.ModelChoiceFilter(label='CUE', queryset=Institucion.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    
    class Meta:
        model = Cursante
        fields = [
            'nombre',
            'apellido',
            'ano_egreso',
            'emisor_titulo',
            'ciudad',
            'direccion',
            'telefono',
            'mail_privado',
            'mail_abc',
            'cargo',
            'situacion_revista',
            'cue',
        ]


class CursanteFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(label='Nombre', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    dni = django_filters.CharFilter(label='D.N.I', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    apellido = django_filters.CharFilter(label='Apellido', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    titulo_habilitante = django_filters.ModelChoiceFilter(label='Titulo habilitante', queryset=TituloHabilitante.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'})) 
    ano_egreso = django_filters.CharFilter(label='Año de egreso', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    emisor_titulo = django_filters.ModelChoiceFilter(label='Emisor del titulo', queryset=Institucion.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    ciudad = django_filters.CharFilter(label='Ciudad', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    direccion = django_filters.CharFilter(label='Direccion', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    telefono = django_filters.CharFilter(label='Telefono', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    mail_privado = django_filters.CharFilter(label='Mail privado', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    mail_abc = django_filters.CharFilter(label='Mail ABC', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    cargo  = django_filters.ModelChoiceFilter(label='Cargo', queryset=Cargo.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    situacion_revista = django_filters.ModelChoiceFilter(label='Situación de Revista', queryset=SituacionRevista.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    titulo_curso_aprobado = django_filters.ModelChoiceFilter(label='Titulo curso aprobado', queryset=Curso.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'})) 
    ano_aprobado = django_filters.CharFilter(label='Año en el que se aprobo', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    area_aprobado = django_filters.ModelChoiceFilter(label='Area aprobada', queryset=Area.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    cohorte_aprobado = django_filters.ModelChoiceFilter(label='Cohorte del aprobado', queryset=Cohorte.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    formador_aprobado = django_filters.ModelChoiceFilter(label='Formador aprobado', queryset=Formador.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    cue = django_filters.ModelChoiceFilter(label='CUE', queryset=Institucion.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    
    class Meta:
        model = Cursante
        fields = [
            'nombre',
            'apellido',
            'dni',
            'titulo_habilitante',
            'ano_egreso',
            'emisor_titulo',
            'ciudad',
            'direccion',
            'telefono',
            'mail_privado',
            'mail_abc',
            'cargo',
            'situacion_revista',
            'titulo_curso_aprobado',
            'ano_aprobado',
            'area_aprobado',
            'cohorte_aprobado',
            'formador_aprobado',
            'cue',
        ]

class CursoFilter(django_filters.FilterSet):
    tipo_dispositivo = django_filters.ModelChoiceFilter(label='Tipo dispositivo', queryset=TipoDispositivo.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    cohorte = django_filters.ModelChoiceFilter(label='Cohorte', queryset=Cohorte.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    nombre_formador = django_filters.ModelChoiceFilter(label='Nombre formador', queryset=Formador.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    modalidad = django_filters.ModelChoiceFilter(label='Modalidad', queryset=Modalidad.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    area = django_filters.ModelChoiceFilter(label='Area', queryset=Area.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    nivel_educativo = django_filters.ModelChoiceFilter(label='Nivel educativo', queryset=NivelEducativo.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    carga_horaria = django_filters.CharFilter(label='Año en el que se aprobo', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    
    class Meta:
        model = Curso
        fields = [
            'tipo_dispositivo',
            'cohorte',
            'nombre_formador',
            'modalidad',
            'area',
            'nivel_educativo',
            'carga_horaria',
        ]

class AsistenciaFilter(django_filters.FilterSet):
    cursante__nombre = django_filters.CharFilter(label='Nombre del cursante', field_name='cursante__nombre', lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    cursante__apellido = django_filters.CharFilter(label='Apellido del cursante', field_name='cursante__apellido', lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    dias_asistidos = django_filters.NumberFilter(label='Días asistidos', field_name='dias_asistidos', lookup_expr='icontains',widget=forms.NumberInput(attrs={'class':'form-control col-sm-8'}))

    class Meta:
        model = AsistenciaCursante
        fields = ['cursante__nombre','cursante__apellido', 'dias_asistidos']


class AprobadoFilter(django_filters.FilterSet):
    cursante__nombre = django_filters.CharFilter(label='Nombre del cursante', field_name='cursante__nombre', lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    cursante__apellido = django_filters.CharFilter(label='Apellido del cursante', field_name='cursante__apellido', lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))

    class Meta:
        model = AsistenciaCursante
        fields = ['cursante__nombre', 'cursante__apellido']

        



class NivelEducativoFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(label='Nombre', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    
    class Meta:
        model = NivelEducativo
        fields = [
            'nombre',
        ]

class ModalidadFilter(django_filters.FilterSet):

    tipo = django_filters.CharFilter(label='Tipo', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    
    class Meta:
        model = Modalidad
        fields = [
            'tipo',
        ]

class TituloHabilitanteFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(label='Nombre', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    nivel_educativo = django_filters.ModelChoiceFilter(label='Nivel educativo', queryset=NivelEducativo.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    
    class Meta:
        model = TituloHabilitante
        fields = [
            'nombre',
            'nivel_educativo',
        ]

class InstitucionFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(label='Nombre', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    modalidad= django_filters.ModelMultipleChoiceFilter(label="Modalidad",queryset=Modalidad.objects.all(), widget=forms.CheckboxSelectMultiple()) 
    nivel_educativo = django_filters.ModelChoiceFilter(label='Nivel educativo', queryset=NivelEducativo.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    cue = django_filters.CharFilter(label='CUE', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    telefono = django_filters.CharFilter(label='Telefono', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    mail = django_filters.CharFilter(label='Mail', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    ciudad = django_filters.CharFilter(label='Ciudad', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    
    class Meta:
        model = Institucion
        fields = [
            'nombre',
            'modalidad',
            'nivel_educativo',
            'cue',
            'telefono',
            'mail',
            'ciudad',
        ]

class CargoFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(label='Nombre', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    nivel_educativo = django_filters.ModelChoiceFilter(label='Nivel educativo', queryset=NivelEducativo.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    
    class Meta:
        model = Cargo
        fields = [
            'nombre',
            'nivel_educativo',
        ]

class SituacionRevistaFilter(django_filters.FilterSet):

    situacion_revista = django_filters.CharFilter(label='Situacion revista', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    
    class Meta:
        model = SituacionRevista
        fields = [
            'situacion_revista',
        ]

class TipoDispositivoFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(label='Nombre', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    resolucion = django_filters.CharFilter(label='Resolucion', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    proyecto = django_filters.CharFilter(label='Proyecto', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    cantidad_horas = django_filters.CharFilter(label='Cantidad horas', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    dictamen = django_filters.CharFilter(label='Dictamen', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control'}))
    puntaje = django_filters.NumberFilter(label='Puntaje', widget=forms.TextInput(attrs={'class':'form-control','type':'number','min':'0','step':'.01'}))
    
    class Meta:
        model = TipoDispositivo
        fields = [
            'nombre',
            'resolucion',
            'proyecto',
            'cantidad_horas',
            'dictamen',
            'puntaje',
        ]

class FormadorFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(label='Nombre', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    apellido = django_filters.CharFilter(label='Apellido', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    
    class Meta:
        model = Formador
        fields = [
            'nombre',
            'apellido',
        ]

class ServiciosFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(label='Nombre', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    
    class Meta:
        model = Servicios
        fields = [
            'nombre',
        ]

class CohorteFilter(django_filters.FilterSet):

    nombre_servicio = django_filters.ModelChoiceFilter(label='Nombre servicio', queryset=Servicios.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    ano = django_filters.CharFilter(label='Año', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    
    class Meta:
        model = Cohorte
        fields = [
        ]

class AreaFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(label='Nombre', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
    
    class Meta:
        model = Area
        fields = [
            'nombre',
        ]

# MODELO BASE

# class preFilter(django_filters.FilterSet):

#     nombre = django_filters.CharFilter(label='Nombre', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control col-sm-8'}))
#     situacion_revista = django_filters.ModelChoiceFilter(label='Situación de Revista', queryset=SituacionRevista.objects.all(), widget=forms.Select(attrs={'class':'form-control col-sm-8'}))
    
#     class Meta:
#         model = pre
#         fields = [
#         ]