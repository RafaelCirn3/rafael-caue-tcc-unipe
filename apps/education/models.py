from django.db import models
from django.conf import settings


class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class ConteudoEducacional(TimeStampedModel):
	class Tipo(models.TextChoices):
		ARTIGO = 'ARTIGO', 'Artigo'
		DICA = 'DICA', 'Dica financeira'
		CURIOSIDADE = 'CURIOSIDADE', 'Curiosidade'
		CONCEITO = 'CONCEITO', 'Conceito'

	titulo = models.CharField(max_length=180)
	descricao = models.TextField()
	tipo = models.CharField(max_length=20, choices=Tipo.choices)
	duracao = models.PositiveIntegerField(default=1)
	ativo = models.BooleanField(default=True)

	class Meta:
		ordering = ['id']


class ProgressoEducacional(TimeStampedModel):
	usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progresso_educacional')
	conteudo = models.ForeignKey(ConteudoEducacional, on_delete=models.CASCADE, related_name='progresso')
	concluido = models.BooleanField(default=False)
	data_conclusao = models.DateTimeField(null=True, blank=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['usuario', 'conteudo'], name='uniq_progresso_usuario_conteudo')
		]
