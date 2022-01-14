from django.test import TestCase

# Create your tests here.
class UsersTest(TestCase):
    def test_users_page(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
