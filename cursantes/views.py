import json
import os
from django.core.files import File
from django.core.files.base import ContentFile
from time import strftime
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import UpdateView
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from .filters import CursanteFilter, CursoFilter, FormadorFilter, InstitucionFilter, ModalidadFilter, SituacionRevistaFilter, TipoDispositivoFilter, TituloHabilitanteFilter, CohorteFilter, CargoFilter, AreaFilter, ServiciosFilter, NivelEducativoFilter, AspiranteFilter,AprobadoFilter,AsistenciaFilter
from legajo_digital.models import Aspirante
from legajo_digital.forms import AspiranteForm


from .forms import CursanteForm, CursoForm, FormadorForm, InstitucionForm, ModalidadForm, SituacionRevistaForm, TipoDispositivoForm, TituloHabilitanteForm, CohorteForm, CargoForm, AreaForm, ServicioForm, NivelEducativoForm,AsistenciasForm,AprobadosForm
from .models import Cursante, Curso, Formador, Institucion, Modalidad, SituacionRevista, TipoDispositivo, TituloHabilitante, Cohorte, Cargo, Area, Servicios, NivelEducativo,AsistenciaCursante,AprobadosCursante
from django.views import View
# Create your views here.

def inicio(request):
    return render(request, 'pagina/inicio.html')
#-------------------LEGAJO-----------------------
def BusquedaDeLegajo (request): 
    #Esta view se encarga de hacer una query con los datos recibidos de parte del cliente
    #Se utiliza una view que envia y recibe es decir POST,GET
    if request.method == "POST":#si el metodo es de envio 
        data = json.loads(request.body)#carga los datos en formato json
        nombre = data.get("nombre")
        apellido = data.get("apellido")
        dni = data.get("dni")
        
        # Filtrar los objetos Cursante según los criterios proporcionados (nombre, apellido, dni)
        users = Cursante.objects.filter(nombre=nombre,apellido=apellido,dni=dni)
    
        users_list = list(users.values()) #convierte en una lista los datos recibidos por la query
        if(len(users_list) <= 0 ) :  # si la lista es menor e igual a 0
            return JsonResponse({"users":None,"type":"danger","message":"No se ha encontrado legajo"}) # envia los datos como consecuencia con mensaje, tipo de mensaje y los datos del usuario
        else :
            return JsonResponse({'users': users_list[0],"type":"success","message":"Legajo encontrado"})
    else:#caso contrario lo reenvia a otra página
        return HttpResponseRedirect("cursos/disponibles")





""" 
def cursantes(request):
    cursantes = Cursante.objects.all()
    return r-ender(request, 'cursantes/index.html', {'cursantes': cursantes})

def crear(request):
    formulario = CursanteForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('cursantes')
    return render(request, 'cursantes/crear.html', {'formulario': formulario})
    
def editar(request, id):
    cursante = Cursante.objects.get(id=id)
    formulario = CursanteForm(request.POST or None, request.FILES or None , instance=cursante)
    if formulario.is_valid() and request.POST: 
        formulario.save()
        return redirect('cursantes')
    return render(request, 'cursantes/editar.html', {'formulario': formulario})

def eliminar(request, id):
    cursante = Cursante.objects.get(id=id)
    cursante.delete()
    return redirect('cursantes_list')
"""

# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
#ASPIRANTES

class AspiranteList(PermissionRequiredMixin, generic.ListView):
    model = Aspirante
    permission_required = 'aspirante.view_aspirante'
    context_object_name = 'aspirante_list'
    template_name = 'aspirantes/aspirante_index.html'
    queryset = Aspirante.objects.all()
    paginate_by = 5
    filterset_class = AspiranteFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        return self.filterset.qs.distinct()


# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________


def model_upload(instance, filename):
    if instance.pk:
        old_instance = Aspirante.objects.get(pk=instance.pk)
        old_instance.titulos.delete()
    return 'archivos/titulos/{0}/{1}'.format(strftime('%Y/%m/%d'), filename)

class AspiranteUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Aspirante
    permission_required = 'aspirante.change_aspirante'
    form_class = AspiranteForm
    template_name = "aspirantes/aspirante_form.html"
    success_url = reverse_lazy('aspirante_list')

    def form_valid(self, form):
        # Obtén la instancia del objeto antes de la actualización
        aspirante = self.get_object()

        # Elimina el archivo antiguo si existe
        old_file = aspirante.titulos
        if old_file:
            old_file.delete()

        # Guarda la instancia del formulario sin commit para obtener el objeto actualizado
        aspirante = form.save(commit=False)

        # Garantiza que el directorio 'archivos/titulos/' exista
        directory = 'archivos/titulos/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Transfiere el nuevo archivo PDF
        if aspirante.titulos and os.path.exists(aspirante.titulos.path):
            with open(aspirante.titulos.path, 'rb') as file_content:
                aspirante.titulos.save(os.path.basename(aspirante.titulos.path), ContentFile(file_content.read()), save=True)

        # Guarda la instancia del formulario y actualiza la base de datos
        aspirante.save()
        response = super().form_valid(form)

        return response

# Define la función para eliminar el archivo antes de que se elimine el objeto
@receiver(pre_delete, sender=Aspirante)
def delete_file(sender, instance, **kwargs):
    # Elimina el archivo asociado al campo 'titulos'
    instance.titulos.delete()
    print("Se ha eliminado el archivo correctamente.")

# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________

# Define la función para eliminar el archivo antes de que se elimine el objeto
@receiver(pre_delete, sender=Aspirante)
def delete_file(sender, instance, **kwargs):
    # Elimina el archivo asociado al campo 'titulos'
    instance.titulos.delete()
    print("Se ha eliminado el archivo correctamente.")

# verificar q es esta cosa pq me estoy quemando por el calor. Con amor Alexis
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________

def delete_aspirante_file(sender, instance, **kwargs):
    # Verifica si el campo 'titulos' contiene un archivo antes de intentar eliminarlo
    if instance.titulos:
        instance.titulos.delete()
        print("Se ha eliminado el archivo asociado al aspirante correctamente.")

@receiver(pre_delete, sender=Aspirante)
def delete_aspirante_file(sender, instance, **kwargs):
    instance.titulos.delete()
    print("Se ha eliminado el archivo correctamente.")

def model_upload(instance, filename):
    if instance.pk:
        old_instance = Aspirante.objects.get(pk=instance.pk)
        old_instance.titulos.delete()
    return 'archivos/titulos/{0}/{1}'.format(strftime('%Y/%m/%d'), filename)

class AspiranteDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Aspirante
    permission_required = 'aspirante.delete_aspirante'
    template_name = "aspirantes/aspirante_delete.html"
    success_url = reverse_lazy('aspirante_list')

    def delete(self, request, *args, **kwargs):
        # Accede al objeto que se va a eliminar
        aspirante = self.get_object()

        # Llama a la función de eliminación del archivo antes de eliminar el objeto
        delete_aspirante_file(sender=Aspirante, instance=aspirante)

        # Llama al método delete original para eliminar el objeto
        return super().delete(request, *args, **kwargs)

    def form_valid(self, form):
        # Accede al objeto que se va a eliminar
        aspirante = self.get_object()

        # Llama a la función de eliminación del archivo antes de eliminar el objeto
        delete_aspirante_file(sender=Aspirante, instance=aspirante)

        # Llama al método form_valid original para continuar con la lógica de eliminación
        return super().form_valid(form)
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________


class AspiranteValidate(PermissionRequiredMixin, generic.DeleteView, generic.UpdateView):
    model = Aspirante
    permission_required = 'aspirantes.change_aspirante'
    form_class = AspiranteForm
    template_name = "aspirantes/aspirante_form.html"
    success_url = reverse_lazy('aspirante_list')

    def form_valid(self, form):
        aspirante = self.get_object()

        try:
            # Crear un nuevo objeto Cursante con los datos de Aspirante
            cursante = Cursante.objects.create(
                nombre=aspirante.nombre,
                apellido=aspirante.apellido,
                dni=aspirante.dni,
                ano_egreso=aspirante.ano_egreso,
                emisor_titulo=aspirante.emisor_titulo,
                ciudad=aspirante.ciudad,
                direccion=aspirante.direccion,
                telefono=aspirante.telefono,
                mail_privado=aspirante.mail_privado,
                mail_abc=aspirante.mail_abc,
                cargo=aspirante.cargo,
                situacion_revista=aspirante.situacion_revista,
                cue=aspirante.cue,
                # titulos es un campo de archivo, por lo que debe ser manejado por separado
            )

            # Garantizar que el directorio 'archivo/titulos_validados/' exista
            directory = 'archivo/titulos_validados/'
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Transferir el archivo PDF
            file_path = str(aspirante.titulos)
            with open(file_path, 'rb') as file_content:
                cursante.titulos.save(os.path.basename(file_path), ContentFile(file_content.read()), save=True)

            # Guardar el nuevo objeto Cursante
            cursante.save()

            # Eliminar el objeto Aspirante original después de haber creado el Cursante
            aspirante.delete()

        except ObjectDoesNotExist as e:
            print(f"Error al eliminar aspirante: {e}")

        return super(AspiranteValidate, self).form_valid(form)
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________

    
#CURSANTES
class CursanteList(PermissionRequiredMixin, generic.ListView):
    model = Cursante
    permission_required = 'cursantes.view_cursante'
    context_object_name = 'cursante_list'
    template_name = 'cursantes/cursante_index.html'
    queryset = Cursante.objects.all()
    paginate_by = 5
    filterset_class = CursanteFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        return self.filterset.qs.distinct()
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________


class CursanteCreate(PermissionRequiredMixin, generic.CreateView):
    model = Cursante
    permission_required = 'cursantes.add_cursante'
    form_class = CursanteForm
    template_name = "cursantes/cursante_form.html"
    success_url = reverse_lazy('cursantes_list')

# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________

def model_upload(instance, filename):
    if instance.pk:
        old_instance = Cursante.objects.get(pk=instance.pk)
        old_instance.titulos.delete()
    return 'archivos/titulos_validados/{0}/{1}'.format(strftime('%Y/%m/%d'), filename)

class CursanteUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Cursante
    permission_required = 'cursantes.change_cursante'
    form_class = CursanteForm
    template_name = "cursantes/cursante_form.html"
    success_url = reverse_lazy('cursantes_list')

    def form_valid(self, form):
        # Obtén la instancia del objeto antes de la actualización
        cursante = self.get_object()

        # Elimina el archivo antiguo si existe
        old_file = cursante.titulos
        if old_file:
            old_file.delete()

        # Guarda la instancia del formulario sin commit para obtener el objeto actualizado
        cursante = form.save(commit=False)

        # Garantiza que el directorio 'archivos/titulos_validados/' exista
        directory = 'archivos/titulos_validados/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Transfiere el nuevo archivo PDF
        if cursante.titulos and os.path.exists(cursante.titulos.path):
            with open(cursante.titulos.path, 'rb') as file_content:
                cursante.titulos.save(os.path.basename(cursante.titulos.path), ContentFile(file_content.read()), save=True)

        # Guarda la instancia del formulario y actualiza la base de datos
        cursante.save()
        response = super().form_valid(form)

        return response

# Define la función para eliminar el archivo antes de que se elimine el objeto
@receiver(pre_delete, sender=Cursante)
def delete_file(sender, instance, **kwargs):
    # Elimina el archivo asociado al campo 'titulos'
    instance.titulos.delete()
    print("Se ha eliminado el archivo correctamente.")
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________

@receiver(pre_delete, sender=Cursante)
def delete_cursante_file(sender, instance, **kwargs):
    instance.titulos.delete()
    print("Se ha eliminado el archivo correctamente.")

def model_upload_cursante(instance, filename):
    if instance.pk:
        old_instance = Cursante.objects.get(pk=instance.pk)
        old_instance.titulos.delete()
    return 'archivos/titulos/{0}/{1}'.format(strftime('%Y/%m/%d'), filename)

class CursanteDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Cursante
    permission_required = 'cursantes.delete_cursante'
    template_name = "cursantes/cursante_delete.html"
    success_url = reverse_lazy('cursantes_list')

    def delete(self, request, *args, **kwargs):
        # Accede al objeto que se va a eliminar
        cursante = self.get_object()

        # Llama a la función de eliminación del archivo antes de eliminar el objeto
        delete_cursante_file(sender=Cursante, instance=cursante)

        # Llama al método delete original para eliminar el objeto
        return super().delete(request, *args, **kwargs)

    def form_valid(self, form):
        # Accede al objeto que se va a eliminar
        cursante = self.get_object()

        # Llama a la función de eliminación del archivo antes de eliminar el objeto
        delete_cursante_file(sender=Cursante, instance=cursante)

        # Llama al método form_valid original para continuar con la lógica de eliminación
        return super().form_valid(form)
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________

# CLASES PARA CURSANTE 


class CursoList(PermissionRequiredMixin, generic.ListView):
    model = Curso
    permission_required = 'cursos.view_curso'
    context_object_name = 'curso_list'
    template_name = 'cursos/curso_index.html'
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

# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________

class CursoCreate(PermissionRequiredMixin, generic.CreateView):
    model = Curso
    permission_required = 'cursos.add_curso'
    form_class = CursoForm
    template_name = 'cursos/curso_form.html'
    success_url = reverse_lazy('curso_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class CursoUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Curso
    permission_required = 'cursos.change_curso'
    form_class = CursoForm
    template_name = "cursos/curso_form.html"
    success_url = reverse_lazy('curso_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class CursoDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Curso
    permission_required = 'cursos.delete_curso'
    template_name = "cursos/curso_delete.html"
    success_url = reverse_lazy('curso_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class CursoDetail(PermissionRequiredMixin, generic.DetailView):
    model = Curso
    permission_required = 'cursos.detail_curso'
    template_name = 'cursos/curso_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso = self.get_object()
        cursantes_asistentes = curso.cursante_set.all()
        context['cursantes_asistentes'] = cursantes_asistentes
        return context
    

class asistencias_curso(PermissionRequiredMixin, generic.ListView):
    model = AsistenciaCursante
    template_name = 'cursos/asistencias_curso.html'
    permission_required = 'cursos.detail_curso'
    filterset_class = AsistenciaFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso_id = self.kwargs.get('pk')
        context['curso'] = Curso.objects.get(pk=curso_id)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        curso_id = self.kwargs.get('pk')
        self.filterset = self.filterset_class(self.request.GET, queryset=AsistenciaCursante.objects.filter(curso__id=curso_id)) 
        return self.filterset.qs.distinct()


class Asistencia_Mark(PermissionRequiredMixin, generic.CreateView):
    model = AsistenciaCursante
    permission_required = 'asistencias.add_asistencias'
    form_class = AsistenciasForm
    template_name = 'cursos/asistencias_form.html'

    def get_success_url(self):
        return reverse_lazy('asistencias_curso', kwargs={'pk': self.kwargs.get('pk')})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        curso_id = self.kwargs.get('pk')
        kwargs['cohorte_deseado'] = str(curso_id)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso_id = self.kwargs.get('pk')
        context['curso'] = Curso.objects.get(pk=curso_id)
        return context

    
class AsistenciasUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = AsistenciaCursante
    permission_required = 'cursos.change_asistencias'
    form_class = AsistenciasForm
    template_name = "cursos/asistencias_form.html"

    def get_success_url(self):
        return reverse_lazy('asistencias_curso', kwargs={'pk': self.object.curso.id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['cohorte_deseado'] = str(self.object.curso.id)
        kwargs['disableCursante'] = self.kwargs.get('pk_cursante')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asistencia_cursante = get_object_or_404(AsistenciaCursante, pk=self.kwargs.get('pk'))
        context['cursante'] = asistencia_cursante.cursante
        context['curso'] = asistencia_cursante.curso
        return context


class AsistenciasDelete(PermissionRequiredMixin, generic.DeleteView):
    model = AsistenciaCursante
    permission_required = 'asistencias.delete_asistencias'
    template_name = "cursos/asistencias_delete.html"

    def get_success_url(self):
        return reverse_lazy('asistencias_curso', kwargs={'pk': self.object.curso.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asistencia_cursante = get_object_or_404(AsistenciaCursante, cursante=self.kwargs.get('pk_cursante'))
        context['curso'] = asistencia_cursante.curso
        return context
    

class aprobados_curso(PermissionRequiredMixin, generic.ListView):
    model = AsistenciaCursante
    template_name = 'cursos/aprobados_curso.html'
    permission_required = 'cursos.detail_curso'
    filterset_class = AprobadoFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso_id = self.kwargs.get('pk')
        context['curso'] = Curso.objects.get(pk=curso_id)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        curso_id = self.kwargs.get('pk')
        self.filterset = self.filterset_class(self.request.GET, queryset=AprobadosCursante.objects.filter(curso__id=curso_id)) 
        return self.filterset.qs.distinct()
    
class Aprobados_Mark(PermissionRequiredMixin, generic.CreateView):
    model = AprobadosCursante
    permission_required = 'aprobados.add_asistencias'
    form_class = AprobadosForm
    template_name = 'cursos/aprobados_form.html'

    def get_success_url(self):
        return reverse_lazy('aprobados_curso', kwargs={'pk': self.kwargs.get('pk')})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        curso_id = self.kwargs.get('pk')
        kwargs['cohorte_deseado'] = str(curso_id)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso_id = self.kwargs.get('pk')
        context['curso'] = Curso.objects.get(pk=curso_id)
        return context
    
class AprobadosUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = AprobadosCursante
    permission_required = 'cursos.change_asistencias'
    form_class = AprobadosForm
    template_name = "cursos/aprobados_form.html"

    def get_success_url(self):
        return reverse_lazy('aprobados_curso', kwargs={'pk': self.object.curso.id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['cohorte_deseado'] = str(self.object.curso.id)
        kwargs['disableCursante'] = self.kwargs.get('pk_cursante')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aprobados_cursante = get_object_or_404(AprobadosCursante, pk=self.kwargs.get('pk'))
        context['cursante'] = aprobados_cursante.cursante
        context['curso'] = aprobados_cursante.curso
        return context
    
class AprobadosDelete(PermissionRequiredMixin, generic.DeleteView):
    model = AprobadosCursante
    permission_required = 'aprobados.delete_aprobados'
    template_name = "cursos/aprobados_delete.html"

    def get_success_url(self):
        return reverse_lazy('aprobados_curso', kwargs={'pk': self.object.curso.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aprobados_cursante = get_object_or_404(AprobadosCursante, cursante=self.kwargs.get('pk_cursante'))
        context['curso'] = aprobados_cursante.curso
        return context
        
# FORMADOR

class FormadorList(PermissionRequiredMixin, generic.ListView):
    model = Formador
    permission_required = 'formador.view_formador'
    context_object_name = 'formador_list'
    template_name = 'formador/formador_index.html'
    queryset = Formador.objects.all()
    filterset_class = FormadorFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        return self.filterset.qs.distinct()
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class FormadorCreate(PermissionRequiredMixin, generic.CreateView):
    model = Formador
    permission_required = 'formador.add_formador'
    form_class = FormadorForm
    template_name = 'formador/formador_form.html'
    success_url = reverse_lazy('formador_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class FormadorUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Formador
    permission_required = 'formador.change_formador'
    form_class = FormadorForm
    template_name = "formador/formador_form.html"
    success_url = reverse_lazy('formador_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class FormadorDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Formador
    permission_required = 'formador.delete_formador'
    template_name = "formador/formador_delete.html"
    success_url = reverse_lazy('formador_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
# INSTITUCION

class InstitucionList(PermissionRequiredMixin, generic.ListView):
    model = Institucion
    permission_required = 'institucion.view_institucion'
    context_object_name = 'institucion_list'
    template_name = 'institucion/institucion_index.html'
    queryset = Institucion.objects.all()
    filterset_class = InstitucionFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        return self.filterset.qs.distinct()
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class InstitucionCreate(PermissionRequiredMixin, generic.CreateView):
    model = Institucion
    permission_required = 'institucion.add_institucion'
    form_class = InstitucionForm
    template_name = 'institucion/institucion_form.html'
    success_url = reverse_lazy('institucion_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class InstitucionUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Institucion
    permission_required = 'institucion.change_institucion'
    form_class = InstitucionForm
    template_name = "institucion/institucion_form.html"
    success_url = reverse_lazy('institucion_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class InstitucionDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Institucion
    permission_required = 'institucion.delete_institucion'
    template_name = "institucion/institucion_delete.html"
    success_url = reverse_lazy('institucion_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
# MODALIDAD

class ModalidadList(PermissionRequiredMixin, generic.ListView):
    model = Modalidad
    permission_required = 'modalidad.view_modalidad'
    context_object_name = 'modalidad_list'
    template_name = 'modalidad/modalidad_index.html'
    queryset = Modalidad.objects.all()
    filterset_class = ModalidadFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        return self.filterset.qs.distinct()
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class ModalidadCreate(PermissionRequiredMixin, generic.CreateView):
    model = Modalidad
    permission_required = 'modalidad.add_modalidad'
    form_class = ModalidadForm
    template_name = 'modalidad/modalidad_form.html'
    success_url = reverse_lazy('modalidad_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class ModalidadUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Modalidad
    permission_required = 'modalidad.change_modalidad'
    form_class = ModalidadForm
    template_name = "modalidad/modalidad_form.html"
    success_url = reverse_lazy('modalidad_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class ModalidadDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Modalidad
    permission_required = 'modalidad.delete_modalidad'
    template_name = "modalidad/modalidad_delete.html"
    success_url = reverse_lazy('modalidad_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
# SITUACION REVISTA 

class SituacionRevistaList(PermissionRequiredMixin, generic.ListView):
    model = SituacionRevista
    permission_required = 'situacionrevista.view_situacionrevista'
    context_object_name = 'situacion_revista_list'
    template_name = 'situacion_revista/situacion_revista_index.html'
    queryset = SituacionRevista.objects.all()
    filterset_class = SituacionRevistaFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        return self.filterset.qs.distinct()
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class SituacionRevistaCreate(PermissionRequiredMixin, generic.CreateView):
    model = SituacionRevista 
    permission_required = 'situacionrevista.add_situacionrevista'
    form_class = SituacionRevistaForm
    template_name = 'situacion_revista/situacion_revista_form.html'
    success_url = reverse_lazy('situacion_revista_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class SituacionRevistaUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = SituacionRevista
    permission_required = 'situacionsevista.change_situacionrevista'
    form_class = SituacionRevistaForm
    template_name = "situacion_revista/situacion_revista_form.html"
    success_url = reverse_lazy('situacion_revista_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class SituacionRevistaDelete(PermissionRequiredMixin, generic.DeleteView):
    model = SituacionRevista
    permission_required = 'situacion_revista.delete_situacionrevista'
    template_name = "situacion_revista/situacion_revista_delete.html"
    success_url = reverse_lazy('situacion_revista_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
# TIPO CURSO 

class TipoDispositivoList(PermissionRequiredMixin, generic.ListView):
    model = TipoDispositivo
    permission_required = 'tipo_dispositivo.view_tipodispositivo'
    context_object_name = 'tipo_dispositivo_list'
    template_name = 'tipo_dispositivo/tipo_dispositivo_index.html'
    queryset = TipoDispositivo.objects.all()
    filterset_class = TipoDispositivoFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        return self.filterset.qs.distinct()
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class TipoDispositivoCreate(PermissionRequiredMixin, generic.CreateView):
    model = TipoDispositivo
    permission_required = 'tipo_dispositivo.add_tipodispositivo'
    form_class = TipoDispositivoForm
    template_name = 'tipo_dispositivo/tipo_dispositivo_form.html'
    success_url = reverse_lazy('tipo_dispositivo_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class TipoDispositivoUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = TipoDispositivo
    permission_required = 'tipo_dispositivo.change_tipodispositivo'
    form_class = TipoDispositivoForm
    template_name = "tipo_dispositivo/tipo_dispositivo_form.html"
    success_url = reverse_lazy('tipo_dispositivo_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class TipoDispositivoDelete(PermissionRequiredMixin, generic.DeleteView):
    model = TipoDispositivo
    permission_required = 'tipo_dispositivo.delete_tipodispositivo'
    template_name = "tipo_dispositivo/tipo_dispositivo_delete.html"
    success_url = reverse_lazy('tipo_dispositivo_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
# TITULO HABILITANTE

class TituloHabilitanteList(PermissionRequiredMixin, generic.ListView):
    model = TituloHabilitante
    permission_required = 'titulo_habilitante.view_titulohabilitante'
    context_object_name = 'titulo_habilitante_list'
    template_name = 'titulo_habilitante/titulo_habilitante_index.html'
    queryset = TituloHabilitante.objects.all()
    filterset_class = TituloHabilitanteFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        return self.filterset.qs.distinct()
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class TituloHabilitanteCreate(PermissionRequiredMixin, generic.CreateView):
    model = TituloHabilitante 
    permission_required = 'titulo_habilitante.add_titulohabilitante'
    form_class = TituloHabilitanteForm
    template_name = 'titulo_habilitante/titulo_habilitante_form.html'
    success_url = reverse_lazy('titulo_habilitante_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class TituloHabilitanteUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = TituloHabilitante
    permission_required = 'titulo_habilitante.change_titulohabilitante'
    form_class = TituloHabilitanteForm
    template_name = "titulo_habilitante/titulo_habilitante_form.html"
    success_url = reverse_lazy('titulo_habilitante_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class TituloHabilitanteDelete(PermissionRequiredMixin, generic.DeleteView):
    model = TituloHabilitante
    permission_required = 'titulo_habilitante.delete_titulohabilitante'
    template_name = "titulo_habilitante/titulo_habilitante_delete.html"
    success_url = reverse_lazy('titulo_habilitante_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
# COHORTE

class CohorteList(PermissionRequiredMixin, generic.ListView):
    model = Cohorte
    permission_required = 'cohorte.view_cohorte'
    context_object_name = 'cohorte_list'
    template_name = 'cohorte/cohorte_index.html'
    queryset = Cohorte.objects.all()
    filterset_class = CohorteFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        return self.filterset.qs.distinct()
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class CohorteCreate(PermissionRequiredMixin, generic.CreateView):
    model = Cohorte 
    permission_required = 'cohorte.add_cohorte'
    form_class = CohorteForm
    template_name = 'cohorte/cohorte_form.html'
    success_url = reverse_lazy('cohorte_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class CohorteUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Cohorte
    permission_required = 'cohorte.change_cohorte'
    form_class = CohorteForm
    template_name = "cohorte/cohorte_form.html"
    success_url = reverse_lazy('cohorte_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
class CohorteDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Cohorte
    permission_required = 'cohorte.delete_cohorte'
    template_name = "cohorte/cohorte_delete.html"
    success_url = reverse_lazy('cohorte_list')
# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________
# CARGO

class CargoList(PermissionRequiredMixin, generic.ListView):
    model = Cargo
    permission_required = 'cargo.view_cargo'
    context_object_name = 'cargo_list'
    template_name = 'cargo/cargo_index.html'
    queryset = Cargo.objects.all()
    filterset_class = CargoFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        return self.filterset.qs.distinct()

class CargoCreate(PermissionRequiredMixin, generic.CreateView):
    model = Cargo 
    permission_required = 'cargo.add_cargo'
    form_class = CargoForm
    template_name = 'cargo/cargo_form.html'
    success_url = reverse_lazy('cargo_list')

class CargoUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Cargo
    permission_required = 'cargo.change_cargo'
    form_class = CargoForm
    template_name = "cargo/cargo_form.html"
    success_url = reverse_lazy('cargo_list')

class CargoDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Cargo
    permission_required = 'cargo.delete_cargo'
    template_name = "cargo/cargo_delete.html"
    success_url = reverse_lazy('cargo_list')

# AREA

class AreaList(PermissionRequiredMixin, generic.ListView):
    model = Area
    permission_required = 'area.view_area'
    context_object_name = 'area_list'
    template_name = 'area/area_index.html'
    queryset = Area.objects.all()
    filterset_class = AreaFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        return self.filterset.qs.distinct()

class AreaCreate(PermissionRequiredMixin, generic.CreateView):
    model = Area 
    permission_required = 'area.add_area'
    form_class = AreaForm
    template_name = 'area/area_form.html'
    success_url = reverse_lazy('area_list')

class AreaUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Area
    permission_required = 'area.change_area'
    form_class = AreaForm
    template_name = "area/area_form.html"
    success_url = reverse_lazy('area_list')

class AreaDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Area
    permission_required = 'area.delete_area'
    template_name = "area/area_delete.html"
    success_url = reverse_lazy('area_list')

# SERVICIO

class ServicioList(PermissionRequiredMixin, generic.ListView):
    model = Servicios
    permission_required = 'servicio.view_servicios'
    context_object_name = 'servicio_list'
    template_name = 'servicio/servicio_index.html'
    queryset = Servicios.objects.all()
    filterset_class = ServiciosFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        return self.filterset.qs.distinct()

class ServicioCreate(PermissionRequiredMixin, generic.CreateView):
    model = Servicios
    permission_required = 'servicio.add_servicios'
    form_class = ServicioForm
    template_name = 'servicio/servicio_form.html'
    success_url = reverse_lazy('servicio_list')

class ServicioUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Servicios
    permission_required = 'servicio.change_servicios'
    form_class = ServicioForm
    template_name = "servicio/servicio_form.html"
    success_url = reverse_lazy('servicio_list')

class ServicioDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Servicios
    permission_required = 'servicio.delete_servicios'
    template_name = "servicio/servicio_delete.html"
    success_url = reverse_lazy('servicio_list')
    
# NIVEL EDUCATIVO

class NivelEducativoList(PermissionRequiredMixin, generic.ListView):
    model = NivelEducativo
    permission_required = 'nivel_educativo.view_curso'
    context_object_name = 'nivel_educativo_list'
    template_name = 'nivel_educativo/nivel_educativo_index.html'
    queryset = NivelEducativo.objects.all()
    filterset_class = NivelEducativoFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        return self.filterset.qs.distinct()

class NivelEducativoCreate(PermissionRequiredMixin, generic.CreateView):
    model = NivelEducativo 
    permission_required = 'nivel_educativo.add_curso'
    form_class = NivelEducativoForm
    template_name = 'nivel_educativo/nivel_educativo_form.html'
    success_url = reverse_lazy('nivel_educativo_list')

class NivelEducativoUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = NivelEducativo
    permission_required = 'nivel_educativo.change_cursante'
    form_class = NivelEducativoForm
    template_name = "nivel_educativo/nivel_educativo_form.html"
    success_url = reverse_lazy('nivel_educativo_list')

class NivelEducativoDelete(PermissionRequiredMixin, generic.DeleteView):
    model = NivelEducativo
    permission_required = 'nivel_educativo.delete_cursante'
    template_name = "nivel_educativo/nivel_educativo_delete.html"
    success_url = reverse_lazy('nivel_educativo_list')

#------------------------------------MOLDE-----------------------------------------# 

# class preList(PermissionRequiredMixin, generic.ListView):
#     model = pre
#     permission_required = 'pre.view_curso'
#     context_object_name = 'pre_list'
#     template_name = 'pre/pre_index.html'
#     queryset = pre.objects.all()

# class preCreate(PermissionRequiredMixin, generic.CreateView):
#     model = pre 
#     permission_required = 'pre.add_curso'
#     form_class = preForm
#     template_name = 'pre/pre_form.html'
#     success_url = reverse_lazy('pre_list')

# class preUpdate(PermissionRequiredMixin, generic.UpdateView):
#     model = pre
#     permission_required = 'pre.change_cursante'
#     form_class = preForm
#     template_name = "pre/pre_form.html"
#     success_url = reverse_lazy('pre_list')

# class preDelete(PermissionRequiredMixin, generic.DeleteView):
#     model = pre
#     permission_required = 'pre.delete_cursante'
#     template_name = "pre/pre_delete.html"
#     success_url = reverse_lazy('pre_list')