from django.contrib import admin

from .models import (Area, Cargo, Cohorte, Cursante, Curso, Formador,
                     Institucion, Modalidad, SituacionRevista, TipoDispositivo,
                     TituloHabilitante, Servicios, NivelEducativo,AsistenciaCursante,
                     AprobadosCursante)

# Register your models here.
admin.site.register(TituloHabilitante)
admin.site.register(Institucion)
admin.site.register(Cargo)
admin.site.register(SituacionRevista)
admin.site.register(Cursante)
admin.site.register(TipoDispositivo)
admin.site.register(Formador)
admin.site.register(Modalidad)
admin.site.register(Cohorte)
admin.site.register(Area)
admin.site.register(Curso)
admin.site.register(Servicios)
admin.site.register(NivelEducativo)
admin.site.register(AsistenciaCursante)
admin.site.register(AprobadosCursante)