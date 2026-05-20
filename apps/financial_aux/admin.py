from django.contrib import admin
from .models import Categoria, Receita, Despesa, MetaFinanceira, Notificacao


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	list_display = ('nome', 'tipo', 'usuario', 'ativa', 'created_at')
	list_filter = ('tipo', 'ativa')
	search_fields = ('nome', 'usuario__email')


@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'valor', 'categoria', 'data')
	list_filter = ('data',)
	search_fields = ('usuario__email', 'descricao')


@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'valor', 'categoria', 'data', 'forma_pagamento')
	list_filter = ('data',)
	search_fields = ('usuario__email', 'descricao', 'forma_pagamento')


@admin.register(MetaFinanceira)
class MetaFinanceiraAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'nome', 'valor_meta', 'valor_atual', 'data_limite')
	list_filter = ('data_limite',)
	search_fields = ('usuario__email', 'nome')


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'tipo', 'titulo', 'lida', 'created_at')
	list_filter = ('tipo', 'lida')
	search_fields = ('usuario__email', 'titulo')
