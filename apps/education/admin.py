from django.contrib import admin
from .models import ConteudoEducacional, ProgressoEducacional


@admin.register(ConteudoEducacional)
class ConteudoEducacionalAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'tipo', 'duracao', 'ativo')
	list_filter = ('tipo', 'ativo')
	search_fields = ('titulo', 'descricao')


@admin.register(ProgressoEducacional)
class ProgressoEducacionalAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'conteudo', 'concluido', 'data_conclusao')
	list_filter = ('concluido',)
	search_fields = ('usuario__email', 'conteudo__titulo')
