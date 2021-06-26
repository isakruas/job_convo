from django.contrib import admin
from .models import (
    Vaga,
    Perfil
)
from .forms import VagaModelForm


@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    form = VagaModelForm
    list_display = (
        'id',
        'registro_pela_empresa',
        'nome',
        'faixa_salarial',
        'requisitos',
        'escolaridade_minima',
        'data_de_registro',
        'data_de_atualizacao',
        'url'
    )


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nome',
        'empresa'
    )
