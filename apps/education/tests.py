from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import ConteudoEducacional, ProgressoEducacional
from rest_framework.test import APIClient


User = get_user_model()


class EducationApiTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create_user(username='eduuser', email='eduuser@example.com', password='SenhaForte123')
		self.login_url = reverse('token_obtain_pair')
		self.conteudos_url = '/api/v1/education/conteudos/'
		self.progresso_url = '/api/v1/education/conteudos/progresso/'

	def authenticate(self):
		response = self.client.post(
			self.login_url,
			data={'email': 'eduuser@example.com', 'password': 'SenhaForte123'},
			content_type='application/json',
		)
		self.assertEqual(response.status_code, 200)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}")

	def test_console_capsule_for_education_flow(self):
		self.authenticate()

		conteudo = ConteudoEducacional.objects.create(
			titulo='Como montar uma reserva',
			descricao='Base do planejamento financeiro.',
			tipo=ConteudoEducacional.Tipo.CONCEITO,
			duracao=5,
			ativo=True,
		)

		list_response = self.client.get(self.conteudos_url)
		print('conteudos_list_status =', list_response.status_code)
		self.assertEqual(list_response.status_code, 200)

		detail_response = self.client.get(f'/api/v1/education/conteudos/{conteudo.id}/')
		print('conteudo_detail_status =', detail_response.status_code)
		self.assertEqual(detail_response.status_code, 200)

		concluir_response = self.client.post(f'/api/v1/education/conteudos/{conteudo.id}/concluir/')
		print('concluir_status =', concluir_response.status_code)
		self.assertEqual(concluir_response.status_code, 200)
		self.assertEqual(self.client.get(self.progresso_url).status_code, 200)

		self.user.refresh_from_db()
		self.assertGreaterEqual(self.user.xp, 10)

	def test_console_capsule_for_progress_persistence(self):
		self.authenticate()
		conteudo = ConteudoEducacional.objects.create(
			titulo='Juros compostos',
			descricao='Conteudo sobre crescimento exponencial.',
			tipo=ConteudoEducacional.Tipo.ARTIGO,
			duracao=8,
			ativo=True,
		)
		progresso, created = ProgressoEducacional.objects.get_or_create(usuario=self.user, conteudo=conteudo)
		print('progresso_created =', created)
		self.assertTrue(created)
		self.assertEqual(progresso.conteudo.titulo, 'Juros compostos')
