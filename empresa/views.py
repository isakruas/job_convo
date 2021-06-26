from django.conf import settings
from django.views.generic import (
    TemplateView,
    ListView,
    UpdateView,
    DeleteView,
    CreateView,
    DetailView
)
from django.urls import reverse_lazy
from .forms import (
    VagaModelForm,
    PerfilModelForm
)
from .models import (
    Vaga as EmpresaVaga,
    Perfil
)
from usuario.models import Usuario
from candidato.models import Vaga as CandidatoVaga
from django.http import HttpResponseRedirect
from functools import wraps
from django.db.models.functions import TruncMonth
from django.db.models import Count


def verificar_acesso_empresa(fn):
    @wraps(fn)
    def get(self, *args, **kwargs):

        if not self.request.user.is_authenticated:
            """
            Só permitir que o usuário acesse o painel após realizar o login
            """
            return HttpResponseRedirect(reverse_lazy('entrar'))

        if self.request.user.get_tipo != 'Empresa':
            """
            Só permitir que o usuário acesse o painel se for registrado com Empresa
            """
            return HttpResponseRedirect(reverse_lazy('entrar'))

        if len(self.request.user.empresa_perfil.all()) == 0:
            """
            Só permitir que o usuário acesse o painel após preencher o perfil
            """
            return HttpResponseRedirect(reverse_lazy('empresa_dashboard_perfil_adicionar'))

        return fn(self, *args, **kwargs)

    return get


class EmpresaVagaDetailView(DetailView):
    template_name = settings.BASE_DIR / 'empresa/templates/vaga_candidato.html'
    model = EmpresaVaga

    @verificar_acesso_empresa
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vaga = kwargs['object']
        __FAIXA_SALARIAL = {
            'Até 1.000': 0,
            'De 1.000 a 2.000': 1,
            'De 2.000 a 3.000': 2,
            'Acima de 3.000': 3,
        }
        __ESCOLARIDADE_MINIMA = {
            'Ensino fundamental': 0,
            'Ensino médio': 1,
            'Tecnólogo': 2,
            'Ensino Superior': 3,
            'Pós / MBA / Mestrado': 4,
            'Doutorado': 5,
        }
        escolaridade_minima = __ESCOLARIDADE_MINIMA.get(vaga.get_escolaridade_minima)
        faixa_salarial = __FAIXA_SALARIAL.get(vaga.get_faixa_salarial)
        candidato = list()
        for __object in CandidatoVaga.objects.filter(vaga=kwargs['object'].id):
            perfil = __object.get_candidato.candidato_perfil.all()[0]
            pontos = 0
            pretensao_salarial = __FAIXA_SALARIAL.get(perfil.get_pretensao_salarial)
            ultima_escolaridade = __ESCOLARIDADE_MINIMA.get(perfil.get_ultima_escolaridade)
            if pretensao_salarial == faixa_salarial:
                pontos += 1
            if ultima_escolaridade >= escolaridade_minima:
                pontos += 1
            el = {
                'perfil': perfil,
                'pontos': pontos
            }
            candidato.append(el)
        context['candidato_vaga_list'] = candidato
        return context


class EmpresaTemplateView(TemplateView):
    template_name = settings.BASE_DIR / 'empresa/templates/dashboard.html'

    @verificar_acesso_empresa
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(EmpresaTemplateView, self).get_context_data(**kwargs)

        candidato_vaga_dados = (candidato.data_de_registro.strftime('%m/%Y') for vaga in
                                EmpresaVaga.objects.filter(registro_pela_empresa=self.request.user) for candidato in
                                CandidatoVaga.objects.filter(vaga=vaga.id))

        candidato_vaga = dict()

        for i, j in enumerate(candidato_vaga_dados):
            if j in candidato_vaga:
                candidato_vaga[str(j)] += 1
            else:
                candidato_vaga[str(j)] = 1

        empresa_vaga_dados = EmpresaVaga.objects.filter(registro_pela_empresa=self.request.user).annotate(
            m=TruncMonth('data_de_registro')).values('m').annotate(c=Count('id')).values('m', 'c')

        empresa_vaga = dict()

        for i in empresa_vaga_dados:
            m = i.get('m').strftime('%m/%Y')
            c = i.get('c')
            empresa_vaga[str(m)] = c

        # candidatos recebidos por mês
        candidato_vaga_x = [k for k, v in candidato_vaga.items()]
        candidato_vaga_y = [v for k, v in candidato_vaga.items()]

        # vagas criadas por mês
        empresa_vaga_x = [k for k, v in empresa_vaga.items()]
        empresa_vaga_y = [v for k, v in empresa_vaga.items()]

        context.update({
            'candidato_vaga_x': candidato_vaga_x,
            'candidato_vaga_y': candidato_vaga_y,
            'empresa_vaga_x': empresa_vaga_x,
            'empresa_vaga_y': empresa_vaga_y,
        })

        return context


class EmpresaPerfilDeleteView(DeleteView):
    template_name = settings.BASE_DIR / 'empresa/templates/perfil_excluir.html'
    model = Usuario
    success_url = reverse_lazy('entrar')

    @verificar_acesso_empresa
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user


class EmpresaPerfilUpdateView(UpdateView):
    template_name = settings.BASE_DIR / 'empresa/templates/perfil_editar.html'
    model = Perfil
    form_class = PerfilModelForm
    success_url = reverse_lazy('empresa_dashboard_perfil')

    @verificar_acesso_empresa
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.empresa_perfil.all()[0]


class EmpresaPerfilDetailView(DetailView):
    template_name = settings.BASE_DIR / 'empresa/templates/perfil.html'
    model = Perfil

    @verificar_acesso_empresa
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.empresa_perfil.all()[0]


class EmpresaPerfilCreateView(CreateView):
    template_name = settings.BASE_DIR / 'empresa/templates/perfil_adicionar.html'
    form_class = PerfilModelForm
    success_url = reverse_lazy('empresa_dashboard')

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            """
            Só permitir que o usuário acesse o painel após realizar o login
            """
            return HttpResponseRedirect(reverse_lazy('entrar'))

        if self.request.user.get_tipo != 'Empresa':
            """
            Só permitir que o usuário acesse o painel se for registrado com Empresa
            """
            return HttpResponseRedirect(reverse_lazy('entrar'))

        if len(self.request.user.empresa_perfil.all()) != 0:
            """
            O usuário já tem um perfil cadastrado
            """
            return HttpResponseRedirect(reverse_lazy('empresa_dashboard_perfil'))

        return super().get(self, *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):

        if len(self.request.user.empresa_perfil.all()) == 0:
            perfil = form.save(commit=False)
            perfil.empresa = self.request.user
            perfil.save()
            return super(EmpresaPerfilCreateView, self).form_valid(form, *args, **kwargs)

        return HttpResponseRedirect(reverse_lazy('empresa_dashboard'))


class EmpresaVagaListView(ListView):
    template_name = settings.BASE_DIR / 'empresa/templates/vaga_listar.html'
    model = EmpresaVaga
    paginate_by = 10
    ordering = '-data_de_registro'

    @verificar_acesso_empresa
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_queryset(self):
        return EmpresaVaga.objects.filter(registro_pela_empresa=self.request.user).order_by('-data_de_registro')


class EmpresaVagaUpdateView(UpdateView):
    template_name = settings.BASE_DIR / 'empresa/templates/vaga_editar.html'
    model = EmpresaVaga
    form_class = VagaModelForm
    success_url = reverse_lazy('empresa_dashboard_vaga')

    @verificar_acesso_empresa
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_queryset(self):
        return EmpresaVaga.objects.filter(registro_pela_empresa=self.request.user)


class EmpresaVagaDeleteView(DeleteView):
    template_name = settings.BASE_DIR / 'empresa/templates/vaga_excluir.html'
    model = EmpresaVaga
    success_url = reverse_lazy('empresa_dashboard_vaga')

    @verificar_acesso_empresa
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_queryset(self):
        return EmpresaVaga.objects.filter(registro_pela_empresa=self.request.user)


class EmpresaVagaCreateView(CreateView):
    template_name = settings.BASE_DIR / 'empresa/templates/vaga_adicionar.html'
    form_class = VagaModelForm
    success_url = reverse_lazy('empresa_dashboard_vaga')

    @verificar_acesso_empresa
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        vaga = form.save(commit=False)
        vaga.registro_pela_empresa = self.request.user
        vaga.save()
        """
        Aqui poderíamos enviar um e-mail para candidatos com perfil que 
        se enquadre nas características descritas na vaga
        """
        return super(EmpresaVagaCreateView, self).form_valid(form, *args, **kwargs)
