from django import template
from cursantes.models import Cohorte, Cursante, Curso

register = template.Library()

@register.simple_tag
def get_cursantes_items(cohorte):
    qs = Cursante.objects.filter(cohorte_aprobado = cohorte)
    return qs
""" 
@register.simple_tag
def get_author_photo(news):
    qs = User_Profile.objects.get(user_profile_user = news.news_author.pk)
    return qs """