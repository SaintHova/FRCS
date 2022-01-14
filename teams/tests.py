from django.test import TestCase

# Create your tests here.
class TeamsTest(TestCase):
    def test_teams(self):
        response = self.client.get('/teams/')
        self.assertEqual(response.status_code, 200)