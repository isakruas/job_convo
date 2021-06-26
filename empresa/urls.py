from django.urls import path

from .views import (
    EmpresaTemplateView,
    EmpresaVagaListView,
    EmpresaVagaUpdateView,
    EmpresaVagaDeleteView,
    EmpresaVagaCreateView,
    EmpresaVagaDetailView,
    EmpresaPerfilCreateView,
    EmpresaPerfilDetailView,
    EmpresaPerfilUpdateView,
    EmpresaPerfilDeleteView
)

urlpatterns = [
    path('dashboard/', EmpresaTemplateView.as_view(), name='empresa_dashboard'),
    path('dashboard/perfil/', EmpresaPerfilDetailView.as_view(), name='empresa_dashboard_perfil'),
    path('dashboard/perfil/adicionar/', EmpresaPerfilCreateView.as_view(), name='empresa_dashboard_perfil_adicionar'),
    path('dashboard/perfil/editar/', EmpresaPerfilUpdateView.as_view(), name='empresa_dashboard_perfil_editar'),
    path('dashboard/perfil/excluir/', EmpresaPerfilDeleteView.as_view(), name='empresa_dashboard_perfil_excluir'),
    path('dashboard/vaga/', EmpresaVagaListView.as_view(), name='empresa_dashboard_vaga'),
    path('dashboard/vaga/adicionar/', EmpresaVagaCreateView.as_view(), name='empresa_dashboard_vaga_adicionar'),
    path('dashboard/vaga/<int:pk>/editar/', EmpresaVagaUpdateView.as_view(), name='empresa_dashboard_vaga_editar'),
    path('dashboard/vaga/<int:pk>/excluir/', EmpresaVagaDeleteView.as_view(), name='empresa_dashboard_vaga_excluir'),
    path('dashboard/vaga/<int:pk>/candidato/', EmpresaVagaDetailView.as_view(), name='empresa_dashboard_vaga_candidato')
]
