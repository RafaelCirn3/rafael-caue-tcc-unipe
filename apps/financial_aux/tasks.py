from datetime import timedelta
from celery import shared_task
from django.db.models import Sum
from django.utils import timezone
from .models import MetaFinanceira, Notificacao, Receita, Despesa


@shared_task
def gerar_lembretes_meta():
    hoje = timezone.now().date()
    limite = hoje + timedelta(days=3)

    metas = MetaFinanceira.objects.filter(data_limite__range=(hoje, limite))
    for meta in metas:
        Notificacao.objects.create(
            usuario=meta.usuario,
            tipo=Notificacao.Tipo.LEMBRETE_META,
            titulo='Meta proxima do vencimento',
            mensagem=f'A meta {meta.nome} vence em {meta.data_limite}.',
        )


@shared_task
def gerar_alertas_financeiros_mensais():
    hoje = timezone.now().date()
    inicio_mes = hoje.replace(day=1)

    despesas = (
        Despesa.objects
        .filter(data__gte=inicio_mes, data__lte=hoje)
        .values('usuario')
        .annotate(total=Sum('valor'))
    )

    receitas_por_usuario = {
        row['usuario']: row['total']
        for row in Receita.objects.filter(data__gte=inicio_mes, data__lte=hoje).values('usuario').annotate(total=Sum('valor'))
    }

    for row in despesas:
        usuario_id = row['usuario']
        total_despesas = row['total'] or 0
        total_receitas = receitas_por_usuario.get(usuario_id, 0) or 0

        if total_despesas > total_receitas:
            Notificacao.objects.create(
                usuario_id=usuario_id,
                tipo=Notificacao.Tipo.ALERTA_FINANCEIRO,
                titulo='Alerta financeiro do mes',
                mensagem='Suas despesas ultrapassaram as receitas neste mes.',
            )
