from django.urls import path
from .views import (
    CandidatoVagaListView,
    CandidatoVagaAllListView,
    CandidatoVagaDeleteView,
    candidato_vaga_candidatar,
    CandidatoPerfilDetailView,
    CandidatoPerfilCreateView,
    CandidatoPerfilUpdateView,
    CandidatoPerfilDeleteView
)

urlpatterns = [
    path('dashboard/', CandidatoVagaListView.as_view(), name='candidato_dashboard'),
    path('dashboard/perfil/', CandidatoPerfilDetailView.as_view(), name='candidato_dashboard_perfil'),
    path('dashboard/perfil/adicionar/', CandidatoPerfilCreateView.as_view(), name='candidato_dashboard_perfil_adicionar'),
    path('dashboard/perfil/editar/', CandidatoPerfilUpdateView.as_view(), name='candidato_dashboard_perfil_editar'),
    path('dashboard/perfil/excluir/', CandidatoPerfilDeleteView.as_view(), name='candidato_dashboard_perfil_excluir'),
    path('dashboard/vaga/', CandidatoVagaAllListView.as_view(), name='candidato_dashboard_vaga'),
    path('dashboard/vaga/<int:pk>/candidatar/', candidato_vaga_candidatar, name='candidato_dashboard_vaga_candidatar'),
    path('dashboard/vaga/<int:pk>/excluir/', CandidatoVagaDeleteView.as_view(), name='candidato_dashboard_vaga_excluir'),
]
