from django import forms
from .models import (
    Perfil
)


class PerfilModelForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nome', 'pretensao_salarial', 'experiencia', 'ultima_escolaridade']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'pretensao_salarial': forms.Select(attrs={'class': 'form-control'}),
            'experiencia': forms.Textarea(attrs={'class': 'form-control'}),
            'ultima_escolaridade': forms.Select(attrs={'class': 'form-control'}),
        }
