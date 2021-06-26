from django.db import models
from usuario.models import Usuario
from django.db.models import signals
from django.template.defaultfilters import slugify
from datetime import datetime
from candidato.models import Vaga as CandidatoVaga


class Perfil(models.Model):
    nome = models.CharField(
        verbose_name='Nome',
        max_length=30,
        blank=None
    )

    empresa = models.ForeignKey(Usuario, verbose_name='Empresa', related_name='empresa_perfil',
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfils'

    @property
    def get_nome(self):
        return self.nome


class Vaga(models.Model):
    nome = models.CharField(verbose_name='Nome da vaga', blank=False, null=False, max_length=200)

    FAIXA_SALARIAL = (
        ('0', 'Até 1.000'),
        ('1', 'De 1.000 a 2.000'),
        ('2', 'De 2.000 a 3.000'),
        ('3', 'Acima de 3.000'),
    )

    faixa_salarial = models.CharField(verbose_name='Faixa salarial', max_length=100, blank=False,
                                      null=False, choices=FAIXA_SALARIAL)

    requisitos = models.TextField(verbose_name='Requisitos', blank=False, null=False, max_length=700)

    ESCOLARIDADE_MINIMA = (
        ('0', 'Ensino fundamental'),
        ('1', 'Ensino médio'),
        ('2', 'Tecnólogo'),
        ('3', 'Ensino Superior'),
        ('4', 'Pós / MBA / Mestrado'),
        ('5', 'Doutorado'),
    )

    escolaridade_minima = models.CharField(verbose_name='Escolaridade mínima', max_length=100, blank=False,
                                           null=False, choices=ESCOLARIDADE_MINIMA)

    data_de_registro = models.DateTimeField(verbose_name='Data de registro', auto_now_add=True, editable=False)

    data_de_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now=True, blank=True, null=True)

    registro_pela_empresa = models.ForeignKey(Usuario, verbose_name='Registro pela empresa', related_name='ofertas',
                                              on_delete=models.CASCADE)

    url = models.SlugField('Url', blank=True, editable=False)

    class Meta:
        verbose_name = 'Vaga'
        verbose_name_plural = 'Vagas'

    def __str__(self):
        return self.nome

    @property
    def get_nome(self):
        return self.nome

    @property
    def get_faixa_salarial(self):
        __FAIXA_SALARIAL = {
            '0': 'Até 1.000',
            '1': 'De 1.000 a 2.000',
            '2': 'De 2.000 a 3.000',
            '3': 'Acima de 3.000',
        }

        return __FAIXA_SALARIAL.get(str(self.faixa_salarial))

    @property
    def get_requisitos(self):
        return self.requisitos

    @property
    def get_escolaridade_minima(self):
        __ESCOLARIDADE_MINIMA = {
            '0': 'Ensino fundamental',
            '1': 'Ensino médio',
            '2': 'Tecnólogo',
            '3': 'Ensino Superior',
            '4': 'Pós / MBA / Mestrado',
            '5': 'Doutorado',
        }
        return __ESCOLARIDADE_MINIMA.get(str(self.escolaridade_minima))

    @property
    def get_registro_pela_empresa(self):
        return self.registro_pela_empresa.get_nome

    @property
    def get_data_de_registro(self):
        return self.data_de_registro.strftime('%d/%m/%Y às %H:%M:%S')

    @property
    def get_url(self):
        return self.url

    @property
    def get_data_de_atualizacao(self):
        return self.data_de_atualizacao.strftime('%d/%m/%Y às %H:%M:%S')


def vaga_pre_save(signal, instance, sender, **kwargs):
    instance.url = slugify(
        f'{instance.nome[0:50]}-{instance.requisitos[0:50]}-{instance.registro_pela_empresa.get_nome[0:50]}-'
        f'{datetime.now().strftime("%y%d%m%H%M%S")}')


def vaga_pre_delete(signal, instance, sender, **kwargs):
    candidato_vaga = CandidatoVaga.objects.filter(vaga=instance.id)
    if candidato_vaga:
        for vaga in candidato_vaga:
            vaga.delete()


signals.pre_save.connect(vaga_pre_save, sender=Vaga)
signals.pre_delete.connect(vaga_pre_delete, sender=Vaga)
