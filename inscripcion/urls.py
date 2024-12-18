from django.urls import path
from .views import *


urlpatterns = [
    path('cursos/disponibles',cursos_disponibles.as_view(),name="cursos_disponibles"),
    path('cursos/inscripcion/<pk>',cursos_inscripcion.as_view(),name="inscripcion")
]


