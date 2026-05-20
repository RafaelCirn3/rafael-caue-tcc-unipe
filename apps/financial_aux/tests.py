from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Categoria, Receita, Despesa, MetaFinanceira
from rest_framework.test import APIClient


User = get_user_model()


class FinancialAuxApiTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create_user(username='finuser', email='finuser@example.com', password='SenhaForte123')
		self.login_url = reverse('token_obtain_pair')
		self.categorias_url = '/api/v1/categorias/'
		self.receitas_url = '/api/v1/receitas/'
		self.despesas_url = '/api/v1/despesas/'
		self.metas_url = '/api/v1/metas/'
		self.dashboard_resumo_url = '/api/v1/dashboard/resumo/'
		self.dashboard_graficos_url = '/api/v1/dashboard/graficos/'

	def authenticate(self):
		response = self.client.post(
			self.login_url,
			data={'email': 'finuser@example.com', 'password': 'SenhaForte123'},
			content_type='application/json',
		)
		self.assertEqual(response.status_code, 200)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}")

	def test_console_capsule_for_financial_flow(self):
		self.authenticate()

		categoria_receita = self.client.post(
			self.categorias_url,
			data={'nome': 'Salario', 'tipo': 'RECEITA'},
			content_type='application/json',
		)
		print('categoria_receita_status =', categoria_receita.status_code)
		self.assertEqual(categoria_receita.status_code, 201)

		categoria_despesa = self.client.post(
			self.categorias_url,
			data={'nome': 'Moradia', 'tipo': 'DESPESA'},
			content_type='application/json',
		)
		print('categoria_despesa_status =', categoria_despesa.status_code)
		self.assertEqual(categoria_despesa.status_code, 201)

		categoria_receita_id = categoria_receita.json()['id']
		categoria_despesa_id = categoria_despesa.json()['id']

		receita_response = self.client.post(
			self.receitas_url,
			data={
				'valor': '2500.00',
				'categoria': categoria_receita_id,
				'descricao': 'Receita principal',
				'data': '2026-05-20',
				'tipo_receita': 'Salario',
			},
			content_type='application/json',
		)
		print('receita_status =', receita_response.status_code)
		self.assertEqual(receita_response.status_code, 201)

		despesa_response = self.client.post(
			self.despesas_url,
			data={
				'valor': '900.00',
				'categoria': categoria_despesa_id,
				'descricao': 'Aluguel',
				'data': '2026-05-20',
				'forma_pagamento': 'PIX',
			},
			content_type='application/json',
		)
		print('despesa_status =', despesa_response.status_code)
		self.assertEqual(despesa_response.status_code, 201)

		meta_response = self.client.post(
			self.metas_url,
			data={
				'nome': 'Reserva de emergencia',
				'valor_meta': '10000.00',
				'valor_atual': '1200.00',
				'data_limite': '2026-12-31',
			},
			content_type='application/json',
		)
		print('meta_status =', meta_response.status_code)
		self.assertEqual(meta_response.status_code, 201)

		resumo_response = self.client.get(self.dashboard_resumo_url)
		print('dashboard_resumo_status =', resumo_response.status_code)
		self.assertEqual(resumo_response.status_code, 200)
		self.assertIn('saldo_atual', resumo_response.json())

		graficos_response = self.client.get(self.dashboard_graficos_url)
		print('dashboard_graficos_status =', graficos_response.status_code)
		self.assertEqual(graficos_response.status_code, 200)
		self.assertIn('receitas_vs_despesas', graficos_response.json())

	def test_console_capsule_for_category_soft_delete(self):
		self.authenticate()
		categoria = Categoria.objects.create(usuario=self.user, nome='Transporte', tipo=Categoria.Tipo.DESPESA)
		response = self.client.delete(f'/api/v1/categorias/{categoria.id}/')
		print('categoria_delete_status =', response.status_code)
		self.assertEqual(response.status_code, 204)
		categoria.refresh_from_db()
		self.assertFalse(categoria.ativa)
