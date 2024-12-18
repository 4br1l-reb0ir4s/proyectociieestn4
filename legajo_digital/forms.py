from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Aspirante


class AspiranteForm(forms.ModelForm):
    class Meta:
        model = Aspirante
        template_name = 'Aspirante_form.html'
        fields = (
        "id",
        "nombre",
        "apellido",
        "dni",
        "ano_egreso",
        "emisor_titulo",
        "ciudad",
        "direccion",
        "telefono",
        "mail_privado",
        "mail_abc",
        "cargo",
        "situacion_revista",
        "cue",
        "titulos")
        labels = {
            "id" : "ID",
            "nombre": "Nombre",
            "apellido":"Apellido",
            "dni":"dni",
            "ano_egreso":"ano de egreso",
            "emisor_titulo":"Emisor del titulo",
            "ciudad":"Ciudad",
            "direccion": "Direccion",
            "telefono": "Telefono",
            "mail_privado":"Mail personal",
            "mail_abc":"Mail ABC",
            "cargo":"Cargo",
            "situacion_revista":"Situacion revista",
            "cue":"CUE",
            "titulos":"titulos"
        }
        widgets = {
            "id": forms.TextInput(attrs={'class':'form-control'}),
            "nombre": forms.TextInput(attrs={'class':'form-control'}),
            "apellido": forms.TextInput(attrs={'class':'form-control'}),
            "dni":forms.TextInput(attrs={'class':'form-control'}),
            "ano_egreso": forms.Select(attrs={'class':'form-select'}),
            "emisor_titulo": forms.Select(attrs={'class':'form-control'}),
            "ciudad": forms.Select(attrs={'class':'form-select'}),
            "direccion": forms.TextInput(attrs={'class':'form-control'}),
            "telefono": forms.TextInput(attrs={'class':'form-control'}),
            "mail_privado": forms.EmailInput(attrs={'class':'form-control'}),
            "mail_abc": forms.EmailInput(attrs={'class':'form-control'}),
            "cargo": forms.Select(attrs={'class':'form-control'}),
            "situacion_revista": forms.Select(attrs={'class':'form-control'}),
            "cue": forms.Select(attrs={'class':'form-control'}),
            'titulos': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_titulos(self):
        titulos = self.cleaned_data.get('titulos')
        if titulos:
            # Verificar si el archivo es un PDF
            if not titulos.name.endswith('.pdf'):
                raise ValidationError(_('El archivo adjunto debe ser un PDF. Se sugiere subir todos los titulos por foto en un PDF'))
        return titulos