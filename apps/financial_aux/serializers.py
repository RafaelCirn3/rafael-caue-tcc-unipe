from decimal import Decimal
from rest_framework import serializers
from .models import Categoria, Receita, Despesa, MetaFinanceira, Notificacao


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id', 'nome', 'tipo', 'ativa', 'usuario', 'created_at', 'updated_at')
        read_only_fields = ('id', 'usuario', 'created_at', 'updated_at')


class ReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receita
        fields = ('id', 'valor', 'categoria', 'descricao', 'data', 'tipo_receita', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_valor(self, value):
        if value <= Decimal('0'):
            raise serializers.ValidationError('O valor da receita deve ser maior que zero.')
        return value

    def validate(self, attrs):
        categoria = attrs.get('categoria')
        if categoria and categoria.tipo != Categoria.Tipo.RECEITA:
            raise serializers.ValidationError({'categoria': 'Categoria invalida para receita.'})
        return attrs


class DespesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesa
        fields = ('id', 'valor', 'categoria', 'descricao', 'data', 'forma_pagamento', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_valor(self, value):
        if value <= Decimal('0'):
            raise serializers.ValidationError('O valor da despesa deve ser maior que zero.')
        return value

    def validate(self, attrs):
        categoria = attrs.get('categoria')
        if categoria and categoria.tipo != Categoria.Tipo.DESPESA:
            raise serializers.ValidationError({'categoria': 'Categoria invalida para despesa.'})
        return attrs


class MetaFinanceiraSerializer(serializers.ModelSerializer):
    percentual_concluido = serializers.SerializerMethodField()

    class Meta:
        model = MetaFinanceira
        fields = (
            'id',
            'nome',
            'valor_meta',
            'valor_atual',
            'data_limite',
            'percentual_concluido',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'percentual_concluido', 'created_at', 'updated_at')

    def validate_valor_meta(self, value):
        if value <= Decimal('0'):
            raise serializers.ValidationError('O valor da meta deve ser maior que zero.')
        return value

    def validate_valor_atual(self, value):
        if value < Decimal('0'):
            raise serializers.ValidationError('O valor atual nao pode ser negativo.')
        return value

    def get_percentual_concluido(self, obj):
        if obj.valor_meta <= 0:
            return 0
        return round(float((obj.valor_atual / obj.valor_meta) * 100), 2)


class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = ('id', 'tipo', 'titulo', 'mensagem', 'lida', 'created_at')
        read_only_fields = ('id', 'created_at')
