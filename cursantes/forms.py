from django import forms
from django.db.models import Subquery, OuterRef
from .models import Cursante, Curso, TituloHabilitante, Institucion, SituacionRevista, Cargo, Formador, Modalidad, TipoDispositivo, Cohorte, Area, Servicios, NivelEducativo,AsistenciaCursante,AprobadosCursante


class CursanteForm(forms.ModelForm):
    class Meta:
        model = Cursante 
        template_name = 'cursantes_form.html'
        fields = (
        "id",
        "legajo",
        "nombre",
        "apellido",
        "dni",
        "titulo_habilitante",
        "ano_egreso",
        "emisor_titulo",
        "ciudad",
        "direccion",
        "telefono",
        "mail_privado",
        "mail_abc",
        "cargo",
        "situacion_revista",
        "titulo_curso_aprobado",
        "ano_aprobado",
        "area_aprobado",
        "cohorte_aprobado",
        "formador_aprobado",
        "cue",
        "titulos")
        labels = {
            "id" : "ID",
            "legajo" : "legajo",
            "nombre": "Nombre",
            "apellido":"Apellido",
            "D.N.I":"D.N.I",
            "titulo_habilitante":"Titulo habilitante",
            "ano_egreso":"ano de egreso",
            "emisor_titulo":"Emisor del titulo",
            "ciudad":"Ciudad",
            "direccion": "Direccion",
            "telefono": "Telefono",
            "mail_privado":"Mail personal",
            "mail_abc":"Mail ABC",
            "cargo":"Cargo",
            "situacion_revista":"Situacion revista",
            "titulo_curso_aprobado":"Titulo de curso aprobado",
            "ano_aprobado":"ano en el que se aprobo",
            "area_aprobado":"Area aprobada",
            "cohorte_aprobado":"Cohorte del aprobado",
            "formador_aprobado":"Formador aprobado",
            "cue":"CUE",
            "titulos":"titulos"
        }
        widgets = {
            
            "id": forms.TextInput(attrs={'class':'form-control'}),
            "legajo": forms.TextInput(attrs={'class':'form-control'}),
            "nombre": forms.TextInput(attrs={'class':'form-control'}),
            "apellido": forms.TextInput(attrs={'class':'form-control'}),
            "dni": forms.TextInput(attrs={'class':'form-control'}),
            "titulo_habilitante": forms.Select(attrs={'class':'form-control'}),
            "ano_egreso": forms.Select(attrs={'class':'form-select'}),
            "emisor_titulo": forms.Select(attrs={'class':'form-control'}),
            "ciudad": forms.Select(attrs={'class':'form-select'}),
            "direccion": forms.TextInput(attrs={'class':'form-control'}),
            "telefono": forms.TextInput(attrs={'class':'form-control'}),
            "mail_privado": forms.EmailInput(attrs={'class':'form-control'}),
            "mail_abc": forms.EmailInput(attrs={'class':'form-control'}),
            "cargo": forms.Select(attrs={'class':'form-control'}),
            "situacion_revista": forms.Select(attrs={'class':'form-control'}),
            "titulo_curso_aprobado": forms.Select(attrs={'class':'form-select'}),
            "ano_aprobado":  forms.Select(attrs={'class':'form-select'}),
            "area_aprobado": forms.Select(attrs={'class':'form-select'}),
            "cohorte_aprobado": forms.Select(attrs={'class':'form-select'}),
            "formador_aprobado": forms.Select(attrs={'class':'form-select'}),
            "cue": forms.Select(attrs={'class':'form-control'}),
            'titulos': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        template_name = 'curso_form.html'
        fields = (
            'id',
            'tipo_dispositivo',
            'cohorte',
            'nombre_formador',
            'modalidad',
            'area',
            'nivel_educativo',
            'carga_horaria'
        )
        labels = {
            'id' : 'ID',
            'tipo_dispositivo': 'Tipo de dispositivo',
            'cohorte': 'Cohorte',
            'nombre_formador': 'Nombre del formador',
            'modalidad': 'Modalidad',
            'area': 'Area',
            'nivel_educativo':'Nivel educativo',
            'carga_horaria':'Carga horaria',
        }
        widgets = {
            'id': forms.TextInput(attrs={'class':'form-control'}),
            'tipo_dispositivo': forms.Select(attrs={'class':'form-control'}),
            'cohorte': forms.Select(attrs={'class':'form-control'}),
            'nombre_formador': forms.Select(attrs={'class':'form-control'}),
            'modalidad': forms.Select(attrs={'class':'form-control'}),
            'area': forms.Select(attrs={'class':'form-control'}),
            'nivel_educativo': forms.Select(attrs={'class':'form-control'}),
            'carga_horaria': forms.TextInput(attrs={'class':'form-control','type':'number','min':'0'})
        }

class AsistenciasForm(forms.ModelForm):
    cursante = forms.ModelChoiceField(
        queryset=Cursante.objects.none(),
        label="Cursantes",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    curso = forms.ModelChoiceField(
        queryset=Curso.objects.none(),
        label="Curso",
        widget=forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        disabled=True,
    )

    def __init__(self, *args, **kwargs):
        cohorte_deseado = kwargs.pop('cohorte_deseado', None)
        disabled = kwargs.pop('disableCursante', None)
        super().__init__(*args, **kwargs)

        if cohorte_deseado:
            if disabled :
                self.fields['cursante'].queryset = Cursante.objects.filter(id=disabled)
            else :
                self.fields['cursante'].queryset = Cursante.objects.filter(
                    cohorte_aprobado=cohorte_deseado
                ).exclude(
                    id__in=Subquery(
                        AsistenciaCursante.objects.filter(cursante=OuterRef('id')).values('cursante')
                    )
                )
            queryFilter=Curso.objects.filter(cohorte=cohorte_deseado)
            self.fields['curso'].queryset = queryFilter
            self.fields['curso'].initial = queryFilter[0]
            if disabled : self.fields['cursante'].disabled=True 

            self.fields['dias_asistidos'].widget.attrs.update({
                'class': 'form-control',
                'max': queryFilter[0].dias_totales_transcurridos
            })

    class Meta:
        model = AsistenciaCursante
        template_name = 'asistencias_form.html'
        fields = (
            "cursante",
            'dias_asistidos',
            'curso'
        )
        labels = {
            'Días asistidos': 'dias_asistidos',
        }
        widgets = {
            'dias_asistidos': forms.NumberInput(),
        }


class AprobadosForm(forms.ModelForm):
    cursante = forms.ModelChoiceField(
        queryset=Cursante.objects.none(),
        label="Cursantes",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    curso = forms.ModelChoiceField(
        queryset=Curso.objects.none(),
        label="Curso",
        widget=forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        disabled=True,
    )

    def __init__(self, *args, **kwargs):
        cohorte_deseado = kwargs.pop('cohorte_deseado', None)
        disabled = kwargs.pop('disableCursante', None)
        super().__init__(*args, **kwargs)

        if cohorte_deseado:
            if disabled :
                self.fields['cursante'].queryset = Cursante.objects.filter(id=disabled)
            else :
                self.fields['cursante'].queryset = Cursante.objects.filter(
                    cohorte_aprobado=cohorte_deseado
                ).exclude(
                    id__in=Subquery(
                        AprobadosCursante.objects.filter(cursante=OuterRef('id')).values('cursante')
                    )
                )
            queryFilter=Curso.objects.filter(cohorte=cohorte_deseado)
            self.fields['curso'].queryset = queryFilter
            self.fields['curso'].initial = queryFilter[0]
            if disabled : self.fields['cursante'].disabled=True 

            self.fields['nota'].widget.attrs.update({
                'class': 'form-control',
                'max': queryFilter[0].dias_totales_transcurridos
            })

    class Meta:
        model = AprobadosCursante
        template_name = 'aprobados_form.html'
        fields = (
            "cursante",
            'nota',
            'curso'
        )
        labels = {
            'nota': 'nota',
        }
        widgets = {
            'nota': forms.NumberInput(),
        }


class TituloHabilitanteForm(forms.ModelForm):
    class Meta: 
        model = TituloHabilitante
        template_name = 'titulo_habilitante_form.html'
        fields = (
            'id',
            'nombre',
            'nivel_educativo'
        )
        labels = {
            'id': 'ID',
            'nombre': 'Nombre',
            'nivel_educativo': 'Nivel educativo'
        }
        widgets = {
            'id': forms.TextInput(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'nivel_educativo': forms.Select(attrs={'class':'form-select'})
        }

class InstitucionForm(forms.ModelForm):
    class Meta: 
        model = Institucion
        template_name = 'institucion_form.html'
        fields = (
            'id',
            'nombre',
            'modalidad',
            'nivel_educativo',
            'cue',
            'telefono',
            'mail',
            'ciudad'
        )
        labels = {
            'id': 'ID',
            'nombre': 'Nombre',
            'modalidad':'Modalidad',
            'nivel_educativo': 'Nivel educativo',
            'cue': 'CUE',
            'telefono': 'Telefono',
            'mail': 'Mail',
            'ciudad': 'Ciudad'
        }
        widgets = {
            'id': forms.TextInput(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'modalidad':forms.CheckboxSelectMultiple(),
            'nivel_educativo': forms.Select(attrs={'class':'form-select'}),
            'cue': forms.TextInput(attrs={'class':'form-control'}),
            'telefono': forms.TextInput(attrs={'class':'form-control'}),
            'mail': forms.EmailInput(attrs={'class':'form-control'}),
            'ciudad': forms.Select(attrs={'class':'form-select'})
        }

class CargoForm(forms.ModelForm):
    class Meta: 
        model = Cargo
        template_name = 'cargo_form.html'
        fields = (
            'id',
            'nombre',
            'nivel_educativo'
        )
        labels = {
            'id': 'ID',
            'nombre': 'Nombre',
            'nivel_educativo': 'Nivel educativo'
        }
        widgets = {
            'id': forms.TextInput(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'nivel_educativo': forms.Select(attrs={'class':'form-select'})
        }

class SituacionRevistaForm(forms.ModelForm):
    class Meta: 
        model = SituacionRevista
        template_name = 'situacion_revista_form.html'
        fields = (
            'id',
            'situacion_revista',
        )
        labels = {
            'id': 'ID',
            'situacion_revista': 'Situacion revista',
        }
        widgets = {
            'id': forms.TextInput(attrs={'class':'form-control'}),
            'situacion_revista': forms.TextInput(attrs={'class':'form-control'}),
        }

class FormadorForm(forms.ModelForm):
    class Meta:
        model = Formador
        template_name = 'formador_form.html'
        fields = (
            'id',
            'nombre',
            'apellido',
        )
        labels = {
            'id': 'ID',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
        }
        widgets = {
            'id': forms.TextInput(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'apellido': forms.TextInput(attrs={'class':'form-control'}),
        }

class ModalidadForm(forms.ModelForm):
    class Meta:
        model = Modalidad
        template_name = 'modalidad_form.html'
        fields = (
            'id',
            'tipo',
        )
        labels = {
            'id': 'ID',
            'tipo': 'Tipo',
        }
        widgets = {
            'id': forms.TextInput(attrs={'class':'form-control'}),
            'tipo': forms.TextInput(attrs={'class':'form-control'}),
        }

class TipoDispositivoForm(forms.ModelForm):
    class Meta:
        model = TipoDispositivo
        template_name = 'tipo_dispositivo_form.html'
        fields = (
            'id',
            'nombre',
            'resolucion',
            'proyecto',
            'cantidad_horas',
            'dictamen',
            'puntaje',
        )
        labels = {
            'id': 'ID',
            'nombre': 'Nombre',
            'resolucion':'Resolucion',
            'proyecto':'Proyecto',
            'cantidad_horas':'Cantidad de horas',
            'dictamen':'Dictamen',
            'puntaje':'Puntaje',
        }
        widgets = {
            'id': forms.TextInput(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'resolucion': forms.TextInput(attrs={'class':'form-control'}),
            'proyecto': forms.TextInput(attrs={'class':'form-control'}),
            'cantidad_horas': forms.TextInput(attrs={'class':'form-control','type':'number','min':'0'}),
            'dictamen': forms.TextInput(attrs={'class':'form-control'}),
            'puntaje': forms.TextInput(attrs={'class':'form-control','type':'number','min':'0','step':'.01'})
        }

class CohorteForm(forms.ModelForm):
    class Meta:
        model = Cohorte
        template_name = 'cohorte_form.html'
        fields = (
            'id',
            'nombre_servicio',
            'ano',
        )
        labels = {
            'id': 'ID',
            'nombre_servicio': 'Nombre servicio',
            'ano': 'ano',
        }
        widgets = {
            'id': forms.TextInput(attrs={'class':'form-control'}),
            'nombre_servicio': forms.Select(attrs={'class':'form-select'}),
            'ano': forms.Select(attrs={'class':'form-select'}),
        }

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        template_name = 'area_form.html'
        fields = (
            'id',
            'nombre',
        )
        labels = {
            'id': 'ID',
            'nombre': 'Nombre',
        }
        widgets = {
            'id': forms.TextInput(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
        }

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicios
        template_name = 'servicio_form.html'
        fields = (
            'id',
            'nombre',
        )
        labels = {
            'id': 'ID',
            'nombre': 'Nombre',
        }
        widgets = {
            'id': forms.TextInput(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
        }    

class NivelEducativoForm(forms.ModelForm):
    class Meta:
        model = NivelEducativo
        template_name = 'nivel_educativo_form.html'
        fields = (
            'id',
            'nombre',
        )
        labels = {
            'id': 'ID',
            'nombre': 'Nombre',
        }
        widgets = {
            'id': forms.TextInput(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
        }