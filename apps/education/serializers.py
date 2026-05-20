from rest_framework import serializers
from .models import ConteudoEducacional, ProgressoEducacional


class ConteudoEducacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConteudoEducacional
        fields = ('id', 'titulo', 'descricao', 'tipo', 'duracao')


class ProgressoEducacionalSerializer(serializers.ModelSerializer):
    conteudo = ConteudoEducacionalSerializer(read_only=True)

    class Meta:
        model = ProgressoEducacional
        fields = ('id', 'conteudo', 'concluido', 'data_conclusao', 'created_at', 'updated_at')
