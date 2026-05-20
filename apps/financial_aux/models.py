from django.conf import settings
from django.db import models
from django.db.models import Q


class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Categoria(TimeStampedModel):
	class Tipo(models.TextChoices):
		RECEITA = 'RECEITA', 'Receita'
		DESPESA = 'DESPESA', 'Despesa'

	usuario = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='categorias',
		null=True,
		blank=True,
	)
	nome = models.CharField(max_length=120)
	tipo = models.CharField(max_length=10, choices=Tipo.choices)
	ativa = models.BooleanField(default=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=['usuario', 'nome', 'tipo'],
				condition=Q(ativa=True),
				name='uniq_categoria_ativa_por_usuario_tipo',
			)
		]
		ordering = ['nome']

	def __str__(self):
		return f'{self.nome} ({self.tipo})'


class Receita(TimeStampedModel):
	usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receitas')
	valor = models.DecimalField(max_digits=12, decimal_places=2)
	categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='receitas')
	descricao = models.CharField(max_length=255, blank=True)
	data = models.DateField()
	tipo_receita = models.CharField(max_length=100, blank=True)

	class Meta:
		ordering = ['-data', '-id']
		indexes = [
			models.Index(fields=['usuario', 'data']),
			models.Index(fields=['usuario', 'categoria']),
		]


class Despesa(TimeStampedModel):
	usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='despesas')
	valor = models.DecimalField(max_digits=12, decimal_places=2)
	categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='despesas')
	descricao = models.CharField(max_length=255, blank=True)
	data = models.DateField()
	forma_pagamento = models.CharField(max_length=100, blank=True)

	class Meta:
		ordering = ['-data', '-id']
		indexes = [
			models.Index(fields=['usuario', 'data']),
			models.Index(fields=['usuario', 'categoria']),
		]


class MetaFinanceira(TimeStampedModel):
	usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='metas_financeiras')
	nome = models.CharField(max_length=120)
	valor_meta = models.DecimalField(max_digits=12, decimal_places=2)
	valor_atual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	data_limite = models.DateField()

	class Meta:
		ordering = ['data_limite', 'id']
		indexes = [models.Index(fields=['usuario', 'data_limite'])]


class Notificacao(TimeStampedModel):
	class Tipo(models.TextChoices):
		LEMBRETE_META = 'LEMBRETE_META', 'Lembrete de meta'
		DICA_FINANCEIRA = 'DICA_FINANCEIRA', 'Nova dica financeira'
		CONCLUSAO_META = 'CONCLUSAO_META', 'Conclusao de meta'
		ALERTA_FINANCEIRO = 'ALERTA_FINANCEIRO', 'Alerta financeiro'

	usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificacoes')
	tipo = models.CharField(max_length=30, choices=Tipo.choices)
	titulo = models.CharField(max_length=120)
	mensagem = models.TextField()
	lida = models.BooleanField(default=False)
