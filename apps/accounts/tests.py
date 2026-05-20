from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.test import APIClient


User = get_user_model()


class AccountsApiTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.register_url = reverse('auth_register')
		self.login_url = reverse('token_obtain_pair')
		self.logout_url = reverse('auth_logout')
		self.me_url = reverse('users_me')
		self.forgot_password_url = reverse('auth_forgot_password')
		self.reset_password_url = reverse('auth_reset_password')

		self.payload = {
			'username': 'rafael',
			'email': 'rafael@example.com',
			'password': 'SenhaForte123',
			'school_name': 'FinanceUp School',
			'city': 'Sao Paulo',
			'state': 'SP',
			'avatar': 'https://example.com/avatar.png',
			'financial_goal': '1500.00',
			'preferences': {'theme': 'dark'},
			'financial_profile': {'income': 5000},
		}

	def test_console_capsule_for_auth_flow(self):
		register_response = self.client.post(self.register_url, data=self.payload, content_type='application/json')
		print('register_status =', register_response.status_code)
		self.assertEqual(register_response.status_code, 201)

		login_response = self.client.post(
			self.login_url,
			data={'email': self.payload['email'], 'password': self.payload['password']},
			content_type='application/json',
		)
		print('login_status =', login_response.status_code)
		self.assertEqual(login_response.status_code, 200)

		tokens = login_response.json()
		self.assertIn('access', tokens)
		self.assertIn('refresh', tokens)

		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

		me_response = self.client.get(self.me_url)
		print('me_status =', me_response.status_code)
		self.assertEqual(me_response.status_code, 200)
		self.assertEqual(me_response.json()['email'], self.payload['email'])

		update_response = self.client.put(
			self.me_url,
			data={
				'username': 'rafael',
				'school_name': 'FinanceUp School',
				'city': 'Rio de Janeiro',
				'state': 'RJ',
				'avatar': 'https://example.com/avatar.png',
				'financial_goal': '2000.00',
				'preferences': {'theme': 'light'},
				'financial_profile': {'income': 6000},
			},
			content_type='application/json',
		)
		print('update_status =', update_response.status_code)
		self.assertEqual(update_response.status_code, 200)
		self.assertEqual(update_response.json()['city'], 'Rio de Janeiro')

		logout_response = self.client.post(
			self.logout_url,
			data={'refresh': tokens['refresh']},
			content_type='application/json',
		)
		print('logout_status =', logout_response.status_code)
		self.assertEqual(logout_response.status_code, 204)

	def test_console_capsule_for_password_reset(self):
		user = User.objects.create_user(
			username='john',
			email='john@example.com',
			password='SenhaForte123',
		)
		forgot_response = self.client.post(
			self.forgot_password_url,
			data={'email': user.email},
			content_type='application/json',
		)
		print('forgot_status =', forgot_response.status_code)
		self.assertEqual(forgot_response.status_code, 202)

		uid = urlsafe_base64_encode(force_bytes(user.pk))
		token = default_token_generator.make_token(user)
		reset_response = self.client.post(
			self.reset_password_url,
			data={'uid': uid, 'token': token, 'new_password': 'NovaSenha123'},
			content_type='application/json',
		)
		print('reset_status =', reset_response.status_code)
		self.assertEqual(reset_response.status_code, 200)
