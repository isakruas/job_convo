from django.db import models
from usuario.models import Usuario
from django.core.exceptions import ObjectDoesNotExist


class Perfil(models.Model):
    nome = models.CharField(
        verbose_name='Nome',
        max_length=30,
        blank=None
    )

    PRETENSAO_SALARIAL = (
        ('0', 'Até 1.000'),
        ('1', 'De 1.000 a 2.000'),
        ('2', 'De 2.000 a 3.000'),
        ('3', 'Acima de 3.000'),
    )

    pretensao_salarial = models.CharField(verbose_name='Pretensão salarial', max_length=100, blank=False,
                                          null=False, choices=PRETENSAO_SALARIAL)

    experiencia = models.TextField(verbose_name='Experiência', blank=False, null=False, max_length=700)

    ULTIMA_ESCOLARIDADE = (
        ('0', 'Ensino fundamental'),
        ('1', 'Ensino médio'),
        ('2', 'Tecnólogo'),
        ('3', 'Ensino Superior'),
        ('4', 'Pós / MBA / Mestrado'),
        ('5', 'Doutorado'),
    )

    ultima_escolaridade = models.CharField(verbose_name='Última Escolaridade', max_length=100, blank=False,
                                           null=False, choices=ULTIMA_ESCOLARIDADE)

    candidato = models.ForeignKey(Usuario, verbose_name='Candidato', related_name='candidato_perfil',
                                  on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfils'

    @property
    def get_nome(self):
        return self.nome

    @property
    def get_experiencia(self):
        return self.experiencia

    @property
    def get_pretensao_salarial(self):
        __PRETENSAO_SALARIAL = {
            '0': 'Até 1.000',
            '1': 'De 1.000 a 2.000',
            '2': 'De 2.000 a 3.000',
            '3': 'Acima de 3.000',
        }

        return __PRETENSAO_SALARIAL.get(str(self.pretensao_salarial))

    @property
    def get_ultima_escolaridade(self):
        __ULTIMA_ESCOLARIDADE = {
            '0': 'Ensino fundamental',
            '1': 'Ensino médio',
            '2': 'Tecnólogo',
            '3': 'Ensino Superior',
            '4': 'Pós / MBA / Mestrado',
            '5': 'Doutorado',
        }
        return __ULTIMA_ESCOLARIDADE.get(str(self.ultima_escolaridade))


class Vaga(models.Model):

    def __init__(self, *args, **kwargs):
        super(Vaga, self).__init__(*args, **kwargs)
        try:
            from empresa.models import Vaga as EmpresaVaga
            self.empresa_vaga = EmpresaVaga.objects.get(id=int(args[2]))
        except (IndexError, ObjectDoesNotExist):
            self.empresa_vaga = None

    candidato = models.ForeignKey(Usuario, verbose_name='Candidato', related_name='vagas',
                                  on_delete=models.CASCADE)
    vaga = models.PositiveIntegerField()

    data_de_registro = models.DateTimeField(verbose_name='Data de registro', auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'Vaga'
        verbose_name_plural = 'Vagas'

    def __str__(self):
        return self.get_vaga.nome

    @property
    def get_candidato(self):
        return self.candidato

    @property
    def get_vaga(self):
        return self.empresa_vaga

    @property
    def get_data_de_registro(self):
        return str(self.data_de_registro)
