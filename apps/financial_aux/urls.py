from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet,
    ReceitaViewSet,
    DespesaViewSet,
    MetaFinanceiraViewSet,
    NotificacaoViewSet,
    DashboardResumoView,
    DashboardGraficosView,
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categorias')
router.register(r'receitas', ReceitaViewSet, basename='receitas')
router.register(r'despesas', DespesaViewSet, basename='despesas')
router.register(r'metas', MetaFinanceiraViewSet, basename='metas')
router.register(r'notificacoes', NotificacaoViewSet, basename='notificacoes')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/resumo/', DashboardResumoView.as_view(), name='dashboard_resumo'),
    path('dashboard/graficos/', DashboardGraficosView.as_view(), name='dashboard_graficos'),
]
