from django.urls import path
from .views import (
    VagaListView,
    VagaDetailView
)


urlpatterns = [
    path('', VagaListView.as_view(), name='vaga'),
    path('vaga/<slug:url>/', VagaDetailView.as_view(), name='vaga_url'),
]
