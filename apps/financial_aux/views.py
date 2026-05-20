from decimal import Decimal
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Categoria, Receita, Despesa, MetaFinanceira, Notificacao
from .serializers import (
	CategoriaSerializer,
	ReceitaSerializer,
	DespesaSerializer,
	MetaFinanceiraSerializer,
	NotificacaoSerializer,
)
from .permissions import IsOwnerOrGlobalReadOnly


class CategoriaViewSet(viewsets.ModelViewSet):
	serializer_class = CategoriaSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrGlobalReadOnly)

	def get_queryset(self):
		queryset = Categoria.objects.filter(ativa=True).filter(usuario=self.request.user) | Categoria.objects.filter(ativa=True, usuario__isnull=True)
		tipo = self.request.query_params.get('tipo')
		if tipo:
			queryset = queryset.filter(tipo=tipo.upper())
		return queryset.order_by('nome').distinct()

	def perform_create(self, serializer):
		serializer.save(usuario=self.request.user)

	def perform_destroy(self, instance):
		if instance.usuario is None:
			return
		instance.ativa = False
		instance.save(update_fields=['ativa'])


class BaseOwnedModelViewSet(viewsets.ModelViewSet):
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		return self.queryset.filter(usuario=self.request.user)

	def perform_create(self, serializer):
		serializer.save(usuario=self.request.user)


class ReceitaViewSet(BaseOwnedModelViewSet):
	serializer_class = ReceitaSerializer
	queryset = Receita.objects.select_related('categoria')

	def get_queryset(self):
		queryset = super().get_queryset()
		data_inicio = self.request.query_params.get('data_inicio')
		data_fim = self.request.query_params.get('data_fim')
		categoria = self.request.query_params.get('categoria')
		valor_min = self.request.query_params.get('valor_min')
		valor_max = self.request.query_params.get('valor_max')

		if data_inicio:
			queryset = queryset.filter(data__gte=data_inicio)
		if data_fim:
			queryset = queryset.filter(data__lte=data_fim)
		if categoria:
			queryset = queryset.filter(categoria_id=categoria)
		if valor_min:
			queryset = queryset.filter(valor__gte=valor_min)
		if valor_max:
			queryset = queryset.filter(valor__lte=valor_max)
		return queryset


class DespesaViewSet(BaseOwnedModelViewSet):
	serializer_class = DespesaSerializer
	queryset = Despesa.objects.select_related('categoria')

	def get_queryset(self):
		queryset = super().get_queryset()
		data_inicio = self.request.query_params.get('data_inicio')
		data_fim = self.request.query_params.get('data_fim')
		categoria = self.request.query_params.get('categoria')
		valor_min = self.request.query_params.get('valor_min')
		valor_max = self.request.query_params.get('valor_max')

		if data_inicio:
			queryset = queryset.filter(data__gte=data_inicio)
		if data_fim:
			queryset = queryset.filter(data__lte=data_fim)
		if categoria:
			queryset = queryset.filter(categoria_id=categoria)
		if valor_min:
			queryset = queryset.filter(valor__gte=valor_min)
		if valor_max:
			queryset = queryset.filter(valor__lte=valor_max)
		return queryset


class MetaFinanceiraViewSet(BaseOwnedModelViewSet):
	serializer_class = MetaFinanceiraSerializer
	queryset = MetaFinanceira.objects.all()

	@action(detail=True, methods=['post'])
	def atualizar_progresso(self, request, pk=None):
		meta = self.get_object()
		valor_atual = request.data.get('valor_atual')
		incremento = request.data.get('incremento')

		if valor_atual is not None:
			meta.valor_atual = Decimal(valor_atual)
		elif incremento is not None:
			meta.valor_atual = meta.valor_atual + Decimal(incremento)
		else:
			return Response({'detail': 'Informe valor_atual ou incremento.'}, status=400)

		meta.save(update_fields=['valor_atual', 'updated_at'])
		return Response(self.get_serializer(meta).data)


class DashboardResumoView(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request):
		receitas = Receita.objects.filter(usuario=request.user)
		despesas = Despesa.objects.filter(usuario=request.user)

		data_inicio = request.query_params.get('data_inicio')
		data_fim = request.query_params.get('data_fim')
		if data_inicio:
			receitas = receitas.filter(data__gte=data_inicio)
			despesas = despesas.filter(data__gte=data_inicio)
		if data_fim:
			receitas = receitas.filter(data__lte=data_fim)
			despesas = despesas.filter(data__lte=data_fim)

		total_receitas = receitas.aggregate(total=Sum('valor'))['total'] or Decimal('0')
		total_despesas = despesas.aggregate(total=Sum('valor'))['total'] or Decimal('0')
		saldo = total_receitas - total_despesas
		percentual_economia = Decimal('0')
		percentual_gasto = Decimal('0')

		if total_receitas > 0:
			percentual_economia = ((saldo / total_receitas) * 100).quantize(Decimal('0.01'))
			percentual_gasto = ((total_despesas / total_receitas) * 100).quantize(Decimal('0.01'))

		return Response({
			'saldo_atual': saldo,
			'total_receitas': total_receitas,
			'total_despesas': total_despesas,
			'economia_mes': saldo,
			'percentual_economia': percentual_economia,
			'percentual_gasto': percentual_gasto,
		})


class DashboardGraficosView(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request):
		receitas_mensais = (
			Receita.objects
			.filter(usuario=request.user)
			.annotate(mes=TruncMonth('data'))
			.values('mes')
			.annotate(total=Sum('valor'))
			.order_by('mes')
		)
		despesas_mensais = (
			Despesa.objects
			.filter(usuario=request.user)
			.annotate(mes=TruncMonth('data'))
			.values('mes')
			.annotate(total=Sum('valor'))
			.order_by('mes')
		)
		distribuicao_despesas = (
			Despesa.objects
			.filter(usuario=request.user)
			.values('categoria__nome')
			.annotate(total=Sum('valor'))
			.order_by('-total')
		)

		return Response({
			'receitas_vs_despesas': {
				'receitas': list(receitas_mensais),
				'despesas': list(despesas_mensais),
			},
			'distribuicao_por_categoria': list(distribuicao_despesas),
		})


class NotificacaoViewSet(BaseOwnedModelViewSet):
	serializer_class = NotificacaoSerializer
	queryset = Notificacao.objects.all()

	@action(detail=True, methods=['post'])
	def marcar_lida(self, request, pk=None):
		notificacao = self.get_object()
		notificacao.lida = True
		notificacao.save(update_fields=['lida', 'updated_at'])
		return Response(self.get_serializer(notificacao).data)
