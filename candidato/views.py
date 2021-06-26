from django.conf import settings
from django.views.generic import (
    ListView,
    DeleteView,
    DetailView,
    CreateView,
    UpdateView
)
from django.urls import reverse_lazy
from .models import (
    Vaga as CandidatoVaga,
    Perfil
)
from .forms import PerfilModelForm
from empresa.models import Vaga as EmpresaVaga
from usuario.models import Usuario
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from functools import wraps


def verificar_acesso_candidato(fn):
    @wraps(fn)
    def get(self, *args, **kwargs):
        try:
            if not self.request.user.is_authenticated:
                """
                Só permitir que o usuário acesse o painel após realizar o login
                """
                return HttpResponseRedirect(reverse_lazy('entrar'))

            if self.request.user.get_tipo != 'Candidato':
                """
                Só permitir que o usuário acesse o painel se for registrado com Candidato
                """
                return HttpResponseRedirect(reverse_lazy('entrar'))

            if len(self.request.user.candidato_perfil.all()) == 0:
                """
                Só permitir que o usuário acesse o painel após preencher o perfil
                """
                return HttpResponseRedirect(reverse_lazy('candidato_dashboard_perfil_adicionar'))

            return fn(self, *args, **kwargs)
        except AttributeError:
            if not self.user.is_authenticated:
                """
                Só permitir que o usuário acesse o painel após realizar o login
                """
                return HttpResponseRedirect(reverse_lazy('entrar'))

            if self.user.get_tipo != 'Candidato':
                """
                Só permitir que o usuário acesse o painel se for registrado com Candidato
                """
                return HttpResponseRedirect(reverse_lazy('entrar'))

            if len(self.user.candidato_perfil.all()) == 0:
                """
                Só permitir que o usuário acesse o painel após preencher o perfil
                """
                return HttpResponseRedirect(reverse_lazy('candidato_dashboard_perfil_adicionar'))

            return fn(self, *args, **kwargs)

    return get


@verificar_acesso_candidato
def candidato_vaga_candidatar(self, *args, **kwargs):
    """
    Adiciona um candidato a uma vaga, se ainda não tiver sido adicionado.
    """
    pk = int(mark_safe(kwargs['pk']))
    if len(self.user.vagas.filter(vaga=pk)):
        """
            O candidato já está inscrito para a vaga
        """
        return HttpResponseRedirect(reverse_lazy('candidato_dashboard'))

    """
    Caso o candidato ainda não esteja inscrito para a vaga, inscreva-o
    """
    if len(EmpresaVaga.objects.filter(id=pk)) == 1:
        self.user.vagas.create(vaga=pk).save()
        return HttpResponseRedirect(reverse_lazy('candidato_dashboard'))
    """
    A vaga não está mais disponivel
    """
    return HttpResponseRedirect(reverse_lazy('candidato_dashboard'))


class CandidatoPerfilDeleteView(DeleteView):
    template_name = settings.BASE_DIR / 'candidato/templates/perfil_excluir.html'
    model = Usuario
    success_url = reverse_lazy('entrar')

    @verificar_acesso_candidato
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user


class CandidatoPerfilUpdateView(UpdateView):
    template_name = settings.BASE_DIR / 'candidato/templates/perfil_editar.html'
    model = Perfil
    form_class = PerfilModelForm
    success_url = reverse_lazy('candidato_dashboard_perfil')

    @verificar_acesso_candidato
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.candidato_perfil.all()[0]


class CandidatoPerfilDetailView(DetailView):
    template_name = settings.BASE_DIR / 'candidato/templates/perfil.html'
    model = Perfil

    @verificar_acesso_candidato
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.candidato_perfil.all()[0]


class CandidatoPerfilCreateView(CreateView):
    template_name = settings.BASE_DIR / 'candidato/templates/perfil_adicionar.html'
    form_class = PerfilModelForm
    success_url = reverse_lazy('candidato_dashboard')

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            """
            Só permitir que o usuário acesse o painel após realizar o login
            """
            return HttpResponseRedirect(reverse_lazy('entrar'))

        if self.request.user.get_tipo != 'Candidato':
            """
            Só permitir que o usuário acesse o painel se for registrado com Candidato
            """
            return HttpResponseRedirect(reverse_lazy('entrar'))

        if len(self.request.user.empresa_perfil.all()) != 0:
            """
            O usuário já tem um perfil cadastrado
            """
            return HttpResponseRedirect(reverse_lazy('candidato_dashboard_perfil'))

        return super().get(self, *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):

        if len(self.request.user.empresa_perfil.all()) == 0:
            perfil = form.save(commit=False)
            perfil.candidato = self.request.user
            perfil.save()
            return super(CandidatoPerfilCreateView, self).form_valid(form, *args, **kwargs)

        return HttpResponseRedirect(reverse_lazy('empresa_dashboard'))


class CandidatoVagaDeleteView(DeleteView):
    template_name = settings.BASE_DIR / 'candidato/templates/vaga_excluir.html'
    model = CandidatoVaga
    success_url = reverse_lazy('candidato_dashboard')

    @verificar_acesso_candidato
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.vagas.all()


class CandidatoVagaListView(ListView):
    template_name = settings.BASE_DIR / 'candidato/templates/dashboard.html'
    model = CandidatoVaga
    paginate_by = 10
    ordering = '-data_de_registro'

    @verificar_acesso_candidato
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CandidatoVagaListView, self).get_context_data(**kwargs)
        candidato_vaga = (vaga.get_vaga.id for vaga in self.request.user.vagas.all())
        empresa_vaga = EmpresaVaga.objects.order_by('-data_de_registro').exclude(id__in=candidato_vaga)[0:3]
        context['empresa_vaga'] = empresa_vaga
        return context

    def get_queryset(self):
        return CandidatoVaga.objects.filter(candidato=self.request.user).order_by('-data_de_registro')


class CandidatoVagaAllListView(ListView):
    template_name = settings.BASE_DIR / 'candidato/templates/vaga_listar.html'
    model = CandidatoVaga
    paginate_by = 10
    ordering = '-data_de_registro'

    @verificar_acesso_candidato
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            candidato_vaga = (vaga.get_vaga.id for vaga in self.request.user.vagas.all())
            return EmpresaVaga.objects.order_by('-data_de_registro').exclude(id__in=candidato_vaga)
        return EmpresaVaga.objects.none()
