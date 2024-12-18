from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views
from .views import *


urlpatterns = [
    path('', views.inicio, name = 'inicio'),
    path('Buscar_Legajo', BusquedaDeLegajo, name = 'Buscar_Legajo'),

    #ASPIRANTES
    path('aspirante', AspiranteList.as_view(), name = 'aspirante_list'),
    path('aspirante/eliminar/<pk>', AspiranteDelete.as_view(), name='eliminar_aspirante'),
    path('aspirante/editar/<pk>', AspiranteUpdate.as_view(), name = 'editar_aspirante'),

    #ASPIRANTE A CURSANTE
    path('aspirante/validar/<pk>', AspiranteValidate.as_view(), name = 'validar_aspirante'),

    # CURSANTES

    path('cursantes', CursanteList.as_view(), name = 'cursantes_list'),
    path('cursantes/crear', CursanteCreate.as_view(), name = 'crear_cursante'),
    path('cursantes/eliminar/<pk>', CursanteDelete.as_view(), name='eliminar_cursante'),
    path('cursantes/editar/<pk>', CursanteUpdate.as_view(), name = 'editar_cursante'),
    
    # CURSOS

    path('cursos', CursoList.as_view(), name = 'curso_list'),
    path('cursos/crear', CursoCreate.as_view(), name = 'crear_curso'),
    path('cursos/eliminar/<pk>', CursoDelete.as_view(), name='eliminar_curso'),
    path('cursos/editar/<pk>', CursoUpdate.as_view(), name = 'editar_curso'),
    path('cursos/detalle/<pk>', CursoDetail.as_view(), name = 'detalle_curso'),


    #asistencias

    path('asistencias/<pk>', asistencias_curso.as_view(), name='asistencias_curso'),
    path('asistencias/<pk>/editar/<int:pk_cursante>', AsistenciasUpdate.as_view(), name='asistencias_edit_cursante'),
    path('asistencias/mark/<pk>', Asistencia_Mark.as_view(), name='asistencias_mark'),
    path('asistencias/<pk>/eliminar/<int:pk_cursante>', AsistenciasDelete.as_view(), name='eliminar_asistencia'),

    #aprobados
    path('aprobados/<pk>', aprobados_curso.as_view(), name='aprobados_curso'),
    path('aprobados/mark/<pk>', Aprobados_Mark.as_view(), name='aprobados_mark'),
    path('aprobados/<pk>/eliminar/<int:pk_cursante>', AprobadosDelete.as_view(), name='eliminar_aprobados'),
    path('aprobados/<pk>/editar/<int:pk_cursante>', AprobadosUpdate.as_view(), name='aprobados_edit_cursante'),
    # FORMADOR

    path('formador', FormadorList.as_view(), name = 'formador_list'),
    path('formador/crear', FormadorCreate.as_view(), name = 'crear_formador'),
    path('formador/eliminar/<pk>', FormadorDelete.as_view(), name='eliminar_formador'),
    path('formador/editar/<pk>', FormadorUpdate.as_view(), name = 'editar_formador'),

    # INSTITUCION

    path('institucion', InstitucionList.as_view(), name = 'institucion_list'),
    path('institucion/crear', InstitucionCreate.as_view(), name = 'crear_institucion'),
    path('institucion/eliminar/<pk>', InstitucionDelete.as_view(), name='eliminar_institucion'),
    path('institucion/editar/<pk>', InstitucionUpdate.as_view(), name = 'editar_institucion'),
    
    # MODALIDAD

    path('modalidad', ModalidadList.as_view(), name = 'modalidad_list'),
    path('modalidad/crear', ModalidadCreate.as_view(), name = 'crear_modalidad'),
    path('modalidad/eliminar/<pk>', ModalidadDelete.as_view(), name='eliminar_modalidad'),
    path('modalidad/editar/<pk>', ModalidadUpdate.as_view(), name = 'editar_modalidad'),

    # SITUACION REVISTA
    
    path('situacion_revista', SituacionRevistaList.as_view(), name = 'situacion_revista_list'),
    path('situacion_revista/crear', SituacionRevistaCreate.as_view(), name = 'crear_situacion_revista'),
    path('situacion_revista/eliminar/<pk>', SituacionRevistaDelete.as_view(), name='eliminar_situacion_revista'),
    path('situacion_revista/editar/<pk>', SituacionRevistaUpdate.as_view(), name = 'editar_situacion_revista'),

    # TIPO DISPOSITIVO

    path('tipo_dispositivo', TipoDispositivoList.as_view(), name = 'tipo_dispositivo_list'),
    path('tipo_dispositivo/crear', TipoDispositivoCreate.as_view(), name = 'crear_tipo_dispositivo'),
    path('tipo_dispositivo/eliminar/<pk>', TipoDispositivoDelete.as_view(), name='eliminar_tipo_dispositivo'),
    path('tipo_dispositivo/editar/<pk>', TipoDispositivoUpdate.as_view(), name = 'editar_tipo_dispositivo'),

    # TITULO HABILITANTE

    path('titulo_habilitante', TituloHabilitanteList.as_view(), name = 'titulo_habilitante_list'),
    path('titulo_habilitante/crear', TituloHabilitanteCreate.as_view(), name = 'crear_titulo_habilitante'),
    path('titulo_habilitante/eliminar/<pk>', TituloHabilitanteDelete.as_view(), name='eliminar_titulo_habilitante'),
    path('titulo_habilitante/editar/<pk>', TituloHabilitanteUpdate.as_view(), name = 'editar_titulo_habilitante'),

    # COHORTE

    path('cohorte', CohorteList.as_view(), name = 'cohorte_list'),
    path('cohorte/crear', CohorteCreate.as_view(), name = 'crear_cohorte'),
    path('cohorte/eliminar/<pk>', CohorteDelete.as_view(), name='eliminar_cohorte'),
    path('cohorte/editar/<pk>', CohorteUpdate.as_view(), name = 'editar_cohorte'),
    

    # CARGO

    path('cargo', CargoList.as_view(), name = 'cargo_list'),
    path('cargo/crear', CargoCreate.as_view(), name = 'crear_cargo'),
    path('cargo/eliminar/<pk>', CargoDelete.as_view(), name='eliminar_cargo'),
    path('cargo/editar/<pk>', CargoUpdate.as_view(), name = 'editar_cargo'),

    # AREA

    path('area', AreaList.as_view(), name = 'area_list'),
    path('area/crear', AreaCreate.as_view(), name = 'crear_area'),
    path('area/eliminar/<pk>', AreaDelete.as_view(), name='eliminar_area'),
    path('area/editar/<pk>', AreaUpdate.as_view(), name = 'editar_area'),

    # SERVICIO

    path('servicio', ServicioList.as_view(), name = 'servicio_list'),
    path('servicio/crear', ServicioCreate.as_view(), name = 'crear_servicio'),
    path('servicio/eliminar/<pk>', ServicioDelete.as_view(), name='eliminar_servicio'),
    path('servicio/editar/<pk>', ServicioUpdate.as_view(), name = 'editar_servicio'),

    # NIVEL EDUCATIVO

    path('nivel_educativo', NivelEducativoList.as_view(), name = 'nivel_educativo_list'),
    path('nivel_educativo/crear', NivelEducativoCreate.as_view(), name = 'crear_nivel_educativo'),
    path('nivel_educativo/eliminar/<pk>', NivelEducativoDelete.as_view(), name='eliminar_nivel_educativo'),
    path('nivel_educativo/editar/<pk>', NivelEducativoUpdate.as_view(), name = 'editar_nivel_educativo'),

]
