from django.contrib import admin
from .models import (
    Vaga,
    Perfil
)


@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'candidato',
        'vaga',
        'data_de_registro'
    )


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nome',
        'pretensao_salarial',
        'experiencia',
        'ultima_escolaridade'
    )
