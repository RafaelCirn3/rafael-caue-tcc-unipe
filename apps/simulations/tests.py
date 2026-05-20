from django.test import TestCase
from django.apps import apps


class SimulationsSmokeTests(TestCase):
	def test_console_capsule_for_app_registration(self):
		app_config = apps.get_app_config('simulations')
		print('simulations_app_name =', app_config.name)
		self.assertEqual(app_config.name, 'apps.simulations')
