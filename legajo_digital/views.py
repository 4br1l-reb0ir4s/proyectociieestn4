from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from .models import Aspirante
from .forms import AspiranteForm

class CrearLegajo(PermissionRequiredMixin, generic.CreateView):
    model = Aspirante
    permission_required = 'aspirante.add_legajo'
    form_class = AspiranteForm
    template_name = 'legajo/crear_legajo.html'
    success_url = reverse_lazy('cursos_disponibles')

    def form_valid(self, form):
        aspirante = form.save(commit=False)
        aspirante.titulos = form.cleaned_data['titulos']
        aspirante.save()
        return super().form_valid(form)