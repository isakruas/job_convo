from django import forms
from .models import (
    Vaga,
    Perfil
)


class PerfilModelForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nome']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }


class VagaModelForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['nome', 'faixa_salarial', 'requisitos', 'escolaridade_minima']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'faixa_salarial': forms.Select(attrs={'class': 'form-control'}),
            'requisitos': forms.Textarea(attrs={'class': 'form-control'}),
            'escolaridade_minima': forms.Select(attrs={'class': 'form-control'}),
        }
