from django.http import HttpResponse
from cursantes.models import  Curso
from cursantes.filters import *  
from django.shortcuts import render 
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic
from .models import *
from cursantes.forms import *
# from cursantes.views import CursoList
# Create your views here.
    

class cursos_disponibles(generic.ListView):
    model= Curso
    permission_required = 'Curso.view_Curso'
    context_object_name= "cursos_disponibles"
    template_name = 'cursos/cursos_disponibles.html'
    queryset = Curso.objects.all()
    filterset_class = CursoFilter


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        return self.filterset.qs.distinct()


class cursos_inscripcion(generic.UpdateView):
    model= Curso
    permission_required = 'cursos.change_curso'
    context_object_name= "cursos_inscripcion"
    form_class = CursanteForm
    template_name = 'cursos/cursos_inscripcion.html'

