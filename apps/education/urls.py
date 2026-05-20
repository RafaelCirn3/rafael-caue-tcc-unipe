from django.urls import path
from .views import (
	ConteudoListView,
	ConteudoDetailView,
	ConcluirConteudoView,
	ProgressoUsuarioView,
)

urlpatterns = [
	path('conteudos/', ConteudoListView.as_view(), name='conteudos_list'),
	path('conteudos/<int:pk>/', ConteudoDetailView.as_view(), name='conteudos_detail'),
	path('conteudos/<int:pk>/concluir/', ConcluirConteudoView.as_view(), name='conteudos_concluir'),
	path('conteudos/progresso/', ProgressoUsuarioView.as_view(), name='conteudos_progresso'),
]
