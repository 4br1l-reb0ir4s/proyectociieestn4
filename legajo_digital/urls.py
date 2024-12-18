from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path("crear/",CrearLegajo.as_view(),name="crear_legajo")
    
]