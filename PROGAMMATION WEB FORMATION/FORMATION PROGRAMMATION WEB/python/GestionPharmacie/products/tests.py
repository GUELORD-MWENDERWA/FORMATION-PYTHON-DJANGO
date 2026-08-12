from django.test import TestCase

# Create your tests here.
#
# TestCase fournit un "client" Django (self.client) qui simule des
# requetes HTTP sans lancer de vrai serveur, tres utile pour verifier
# qu'une page repond bien (status_code == 200) ou qu'un formulaire
# cree correctement une ligne en base. Exemple minimal des qu'une vue
# existe :
#
#   class HomeViewTests(TestCase):
#       def test_home_status_code(self):
#           response = self.client.get('/')
#           self.assertEqual(response.status_code, 200)
#
# Lancer les tests du projet : python manage.py test
