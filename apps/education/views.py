from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ConteudoEducacional, ProgressoEducacional
from .serializers import ConteudoEducacionalSerializer, ProgressoEducacionalSerializer


class ConteudoListView(generics.ListAPIView):
	serializer_class = ConteudoEducacionalSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		return ConteudoEducacional.objects.filter(ativo=True)


class ConteudoDetailView(generics.RetrieveAPIView):
	serializer_class = ConteudoEducacionalSerializer
	permission_classes = (permissions.IsAuthenticated,)
	queryset = ConteudoEducacional.objects.filter(ativo=True)


class ConcluirConteudoView(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request, pk):
		conteudo = generics.get_object_or_404(ConteudoEducacional, pk=pk, ativo=True)
		progresso, _ = ProgressoEducacional.objects.get_or_create(usuario=request.user, conteudo=conteudo)

		if not progresso.concluido:
			progresso.concluido = True
			progresso.data_conclusao = timezone.now()
			progresso.save(update_fields=['concluido', 'data_conclusao', 'updated_at'])

			request.user.xp = request.user.xp + 10
			request.user.save(update_fields=['xp'])

		return Response(ProgressoEducacionalSerializer(progresso).data)


class ProgressoUsuarioView(generics.ListAPIView):
	serializer_class = ProgressoEducacionalSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		return ProgressoEducacional.objects.filter(usuario=self.request.user).select_related('conteudo')
