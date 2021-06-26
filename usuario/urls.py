from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.views.decorators.http import require_GET
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .views import (
    UsuarioCreateView,
)


@require_GET
def dashboard(request):
    try:
        if request.user.get_tipo == 'Empresa':
            return HttpResponseRedirect(reverse_lazy('empresa_dashboard'))
        elif request.user.get_tipo == 'Candidato':
            return HttpResponseRedirect(reverse_lazy('candidato_dashboard'))
    except AttributeError:
        return HttpResponseRedirect(reverse_lazy('entrar'))


urlpatterns = [
    path('registrar/', UsuarioCreateView.as_view(), name='registrar'),
    path('', auth_views.LoginView.as_view(
        template_name=settings.BASE_DIR / 'usuario/templates/entrar.html',
    ), name='entrar', ),
    path('sair/', auth_views.LogoutView.as_view(next_page='/'), name='sair'),
    path('dashboard/', dashboard, name='dashboard')
]
