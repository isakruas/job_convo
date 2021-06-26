from django.conf import settings
from django.views.generic import CreateView
from .forms import UsuarioCreateForm
from django.urls import reverse_lazy


class UsuarioCreateView(CreateView):
    template_name = settings.BASE_DIR / 'usuario/templates/registrar.html'
    form_class = UsuarioCreateForm
    success_url = reverse_lazy('entrar')

    def form_valid(self, form, *args, **kwargs):
        """
        Aqui deve-se enviar um email para confirmação de cadastro
        """
        return super(UsuarioCreateView, self).form_valid(form, *args, **kwargs)
