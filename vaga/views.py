from django.conf import settings
from django.views.generic import (
    ListView,
    DetailView
)
from empresa.models import Vaga


class VagaListView(ListView):
    template_name = settings.BASE_DIR / 'vaga/templates/vaga_listar.html'
    model = Vaga
    paginate_by = 10
    ordering = '-data_de_registro'


class VagaDetailView(DetailView):
    template_name = settings.BASE_DIR / 'vaga/templates/vaga_detalhe.html'
    model = Vaga
    query_pk_and_slug = True
    slug_field = 'url'
    slug_url_kwarg = 'url'
