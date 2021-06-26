from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models


class Base(BaseUserManager):
    use_in_migrations = True

    def __create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Não foi possível criar a conta, o email não foi informado.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        return self.__create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Não foi possível criar o superusuário, o parâmetro is_superuser não foi configurado '
                             'como True.')

        if extra_fields.get('is_active') is not True:
            raise ValueError('Não foi possível criar o superusuário, o parâmetro is_active não foi configurado '
                             'como True.')

        return self.__create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    objects = Base()

    TIPO_DE_USUARIO = (
        ('1', 'Empresa'),
        ('2', 'Candidato'),
    )

    tipo = models.CharField(
        verbose_name='Eu quero me registrar como',
        max_length=50,
        null=False,
        blank=False,
        choices=TIPO_DE_USUARIO
    )

    email = models.EmailField(
        'Email',
        max_length=255,
        unique=True,

    )

    is_active = models.BooleanField(default=True)  # default=False

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['tipo']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['id']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def is_admin(self):
        return self.is_superuser

    @property
    def get_tipo(self):
        if self.tipo == '1':
            return 'Empresa'
        return 'Candidato'

    @property
    def get_email(self):
        return self.email

    @property
    def get_nome(self):
        if self.tipo == '1':
            return self.empresa_perfil.all()[0].get_nome
        return self.candidato_perfil.all()[0].get_nome
